from .dashboard_abstract import AbstractDasboard
from typing import List, Any
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
class OrganizationalDashboard (AbstractDasboard):
    streams: List[str] = ["issues"]
    issues_df: Any = None
    monte_carlo_simulations:int = 1000
    output_dir:str = "organization_charts"
    
    def model_post_init(self, __context):
        super().model_post_init(__context)
        self.issues_df = self.cache["issues"].to_pandas()

    
    def compute_stats(self) -> dict:
        """Compute overall organization stats."""
        # Group all issues by state
        state_counts = self.issues_df['state'].value_counts().to_dict()
        
        # Ensure we have open and closed counts
        open_count = state_counts.get('open', 0)
        closed_count = state_counts.get('closed', 0)
        
        # Calculate totals
        total_issues = open_count + closed_count
        percent_closed = round((closed_count / total_issues * 100), 1) if total_issues > 0 else 0
        
        return {
            'open': open_count,
            'closed': closed_count,
            'total': total_issues,
            'percent_closed': percent_closed
        }

    def generate_markdown_header(self, stats: dict) -> str:
        markdown = "# 📈 GitHub Issue Stats - Organização\n\n"
        markdown += "| 🟢 Abertas | 🔴 Fechadas | 📦 Total | ✅ % Fechadas |\n"
        markdown += "|----------|------------|---------|------------|\n"
        markdown += f"| {stats['open']} | {stats['closed']} | {stats['total']} | {stats['percent_closed']}% |\n\n"
        return markdown

    def plot_weekly_delivery(self, weekly_data: pd.DataFrame):
        """Create biweekly delivery chart for the entire organization."""
        filename = f"{self.output_dir}/organization_biweekly.png"
        
        periods = weekly_data["period"].dt.strftime("%Y-%m-%d")
        promised = weekly_data["promised"]
        delivered = weekly_data["delivered"]
        percent_completed = weekly_data["percent_completed"].round(1)
        
        fig, ax1 = plt.subplots(figsize=(12, 5))
        bar_width = 0.4
        x = range(len(periods))
        
        # Bar chart for issues
        ax1.bar([i - bar_width / 2 for i in x], promised, width=bar_width, label="Prometido", color="navy")
        ax1.bar([i + bar_width / 2 for i in x], delivered, width=bar_width, label="Entregue", color="green")
        ax1.set_ylabel("Issues", fontsize=12)
        ax1.set_xticks(x)
        ax1.set_xticklabels(periods, rotation=45)
        ax1.tick_params(axis='y', labelsize=10)
        ax1.legend(loc="upper left", fontsize=10)
        
        # Line chart for completion percentage
        ax2 = ax1.twinx()
        ax2.plot(x, percent_completed, color="darkred", marker="o", linewidth=2, label="% Concluído")
        ax2.set_ylabel("% Concluído", fontsize=12)
        ax2.set_ylim(0, 110)
        ax2.tick_params(axis='y', labelsize=10)
        ax2.legend(loc="upper right", fontsize=10)
        
        plt.title("Entregas Quinzenais da Organização (Ultimos 6 meses)", fontsize=14, pad=20)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        
        return filename

    def plot_burnup_chart(self, weekly_data: pd.DataFrame):
        """Create burnup chart for the entire organization."""
        filename = f"{self.output_dir}/organization_burnup.png"
        
        # Sort by period and calculate cumulative metrics
        df = weekly_data.sort_values("period")
        df["cumulative_promised"] = df["promised"].cumsum()
        df["cumulative_delivered"] = df["delivered"].cumsum()
        
        # Convert periods to list for proper indexing
        periods_list = df["period"].dt.strftime("%Y-%m-%d").tolist()
        x = range(len(periods_list))
        
        plt.figure(figsize=(12, 5))
        
        # Plot the cumulative lines
        plt.plot(x, df["cumulative_promised"], label="Prometido acumulado", color="blue", marker="o", linewidth=2)
        plt.plot(x, df["cumulative_delivered"], label="Entregue acumulado", color="green", marker="o", linewidth=2)
        plt.fill_between(x, df["cumulative_delivered"], df["cumulative_promised"], color="lightgray", alpha=0.3)
        
        # Add trend line and projection if we have enough data
        if len(df) >= 2:
            z = pd.Series(df["cumulative_delivered"].values).interpolate(method='linear')
            trend = pd.Series(z).rolling(window=2, min_periods=1).mean()
            plt.plot(x, trend, linestyle="--", color="orange", label="Tendência", linewidth=2)
            
            total_prometido = df["cumulative_promised"].max()
            if trend.iloc[-1] > 0 and len(trend) >= 2:
                delta = trend.iloc[-1] - trend.iloc[-2]
                if delta > 0:  # Only predict if there's positive progress
                    periods_to_finish = (total_prometido - trend.iloc[-1]) / delta
                    if 0 < periods_to_finish < 20:
                        # Calculate future date - multiply by 14 for days since we're using biweekly periods
                        last_period_date = pd.to_datetime(df["period"].iloc[-1])
                        predicted_date = last_period_date + pd.Timedelta(days=int(periods_to_finish * 14))
                        predicted_date_str = predicted_date.strftime('%Y-%m-%d')
                        
                        # Add vertical line at prediction
                        future_x = len(periods_list) - 1 + periods_to_finish
                        plt.axvline(x=future_x, linestyle=":", color="red", 
                                   label=f"Previsão: {predicted_date_str}", linewidth=2)
        
        plt.xticks(x, periods_list, rotation=45)
        plt.xlabel("Período", fontsize=12)
        plt.ylabel("Issues acumuladas", fontsize=12)
        plt.title("🔥 Burn-up Chart da Organização  (Ultimos 6 meses) ", fontsize=14, pad=20)
        plt.legend(fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        
        return filename, df
        
    def compute_weekly_delivery_stats(self) -> pd.DataFrame:
        """Compute biweekly stats for all issues across all repositories."""
        df = self.issues_df.copy()
        
        # Convert created_at to datetime and get two-week period
        df["created_at"] = pd.to_datetime(df["created_at"])
        # Use 2W for two-week periods instead of W for weekly
        df["period"] = df["created_at"].dt.to_period("2W").apply(lambda r: r.start_time)
        
        # Group by two-week period and state, calculate counts
        grouped = df.groupby(["period", "state"]).size().unstack(fill_value=0)
        
        # Ensure we have open and closed columns
        for col in ["open", "closed"]:
            if col not in grouped.columns:
                grouped[col] = 0
        
        # Calculate additional metrics
        grouped["promised"] = grouped["open"] + grouped["closed"]
        grouped["delivered"] = grouped["closed"]
        grouped["percent_completed"] = (grouped["closed"] / grouped["promised"]).fillna(0) * 100
        
        # Reset index to make period a column
        return grouped.reset_index()
    def run_monte_carlo_simulation(self, weekly_data: pd.DataFrame) -> dict:
        """Run Monte Carlo simulation for organization completion date."""
        # Sort data chronologically
        df = weekly_data.sort_values("period")
        
        # Extract historical velocities
        velocities = df["delivered"].tolist()
        
        # Calculate remaining work
        df["cumulative_promised"] = df["promised"].cumsum()
        df["cumulative_delivered"] = df["delivered"].cumsum()
        remaining_work = df["cumulative_promised"].max() - df["cumulative_delivered"].max()
        
        # If no work left, return completed status
        if remaining_work <= 0:
            return {
                'velocity_mean': np.mean(velocities),
                'velocity_p10': np.percentile(velocities, 10) if len(velocities) > 0 else 0,
                'velocity_p50': np.percentile(velocities, 50) if len(velocities) > 0 else 0,
                'velocity_p90': np.percentile(velocities, 90) if len(velocities) > 0 else 0,
                'completion_date_p10': "Complete",
                'completion_date_p50': "Complete",
                'completion_date_p90': "Complete",
                'simulation_data': [],
            }
        
        # Get last date as starting point
        last_date = pd.to_datetime(df["period"].max())
        
        # Run simulations
        simulation_data = []
        print(f"🎲 Executando {self.monte_carlo_simulations} simulações Monte Carlo...")
        
        for _ in range(self.monte_carlo_simulations):
            # Bootstrap sampling of historical velocities
            sampled_velocities = random.choices(velocities, k=len(velocities))
            
            # Calculate mean velocity with random factor
            mean_velocity = np.mean(sampled_velocities) * random.uniform(0.8, 1.2)
            
            # Skip if velocity is zero or negative
            if mean_velocity <= 0:
                continue
            
            # Calculate periods to completion
            periods_to_completion = remaining_work / mean_velocity
            
            # Calculate completion date - now each period is 14 days (biweekly)
            completion_date = last_date + pd.Timedelta(days=int(periods_to_completion * 14))
            
            # Store simulation results
            simulation_data.append({
                'velocity': mean_velocity,
                'periods_to_completion': periods_to_completion,
                'completion_date': completion_date
            })
        
        # Calculate statistics from simulation results
        if not simulation_data:
            return {
                'velocity_mean': np.mean(velocities) if velocities else 0,
                'velocity_p10': 0, 
                'velocity_p50': 0,
                'velocity_p90': 0,
                'completion_date_p10': None,
                'completion_date_p50': None,
                'completion_date_p90': None,
                'simulation_data': [],
            }
        
        # Extract velocities and completion dates
        all_velocities = [sim['velocity'] for sim in simulation_data]
        all_completion_dates = [sim['completion_date'] for sim in simulation_data]
        
        # Calculate percentiles
        velocity_mean = np.mean(all_velocities)
        velocity_p10 = np.percentile(all_velocities, 10)
        velocity_p50 = np.percentile(all_velocities, 50)
        velocity_p90 = np.percentile(all_velocities, 90)
        
        # Calculate date percentiles
        completion_dates_sorted = sorted(all_completion_dates)
        idx_p10 = min(int(0.1 * len(completion_dates_sorted)), len(completion_dates_sorted) - 1)
        idx_p50 = min(int(0.5 * len(completion_dates_sorted)), len(completion_dates_sorted) - 1)
        idx_p90 = min(int(0.9 * len(completion_dates_sorted)), len(completion_dates_sorted) - 1)
        
        completion_date_p10 = completion_dates_sorted[idx_p10]
        completion_date_p50 = completion_dates_sorted[idx_p50]
        completion_date_p90 = completion_dates_sorted[idx_p90]
        
        print("✅ Simulações Monte Carlo concluídas.")
        
        return {
            'velocity_mean': velocity_mean,
            'velocity_p10': velocity_p10,
            'velocity_p50': velocity_p50,
            'velocity_p90': velocity_p90,
            'completion_date_p10': completion_date_p10.strftime('%Y-%m-%d'),
            'completion_date_p50': completion_date_p50.strftime('%Y-%m-%d'),
            'completion_date_p90': completion_date_p90.strftime('%Y-%m-%d'),
            'simulation_data': simulation_data,
        }

    def plot_monte_carlo_simulations(self, mc_results: dict):
        """Create Monte Carlo visualizations for the organization."""
        if not mc_results['simulation_data']:
            return None, None
        
        # Completion date histogram
        mc_filename = f"{self.output_dir}/organization_monte_carlo.png"
        plt.figure(figsize=(12, 6))
        
        # Extract completion dates
        completion_dates = [sim['completion_date'] for sim in mc_results['simulation_data']]
        
        # Calculate bins
        min_date = min(completion_dates)
        max_date = max(completion_dates)
        weeks_span = (max_date - min_date).days // 7 + 1
        bins = min(weeks_span, 20)
        
        # Convert dates to numerical format
        completion_dates_num = [(date - min_date).days / 7 for date in completion_dates]
        
        # Plot histogram
        plt.hist(completion_dates_num, bins=bins, alpha=0.7, color='blue', edgecolor='black', linewidth=0.5)
        
        # Add percentile lines
        p10_idx = int(len(completion_dates) * 0.1)
        p50_idx = int(len(completion_dates) * 0.5)
        p90_idx = int(len(completion_dates) * 0.9)
        
        sorted_dates_num = sorted(completion_dates_num)
        p10_value = sorted_dates_num[p10_idx] if p10_idx < len(sorted_dates_num) else sorted_dates_num[-1]
        p50_value = sorted_dates_num[p50_idx] if p50_idx < len(sorted_dates_num) else sorted_dates_num[-1]
        p90_value = sorted_dates_num[p90_idx] if p90_idx < len(sorted_dates_num) else sorted_dates_num[-1]
        
        plt.axvline(x=p10_value, color='green', linestyle='--', linewidth=2, label='P10 (Otimista)')
        plt.axvline(x=p50_value, color='orange', linestyle='--', linewidth=2, label='P50 (Provável)')
        plt.axvline(x=p90_value, color='red', linestyle='--', linewidth=2, label='P90 (Conservador)')
        
        # Set x-axis ticks to show dates
        tick_positions = np.linspace(0, max(completion_dates_num), min(10, bins))
        tick_labels = [(min_date + pd.Timedelta(days=int(pos * 7))).strftime('%Y-%m-%d') for pos in tick_positions]
        plt.xticks(tick_positions, tick_labels, rotation=45)
        
        plt.title("🎲 Simulação Monte Carlo - Previsão de Conclusão", fontsize=14, pad=20)
        plt.xlabel("Data de Conclusão Prevista", fontsize=12)
        plt.ylabel("Número de Simulações", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.savefig(mc_filename)
        plt.close()
        
        # Velocity distribution chart
        vel_filename = f"{self.output_dir}/organization_velocity_dist.png"
        plt.figure(figsize=(12, 5))
        
        velocities = [sim['velocity'] for sim in mc_results['simulation_data']]
        plt.hist(velocities, bins=min(20, len(velocities)//5 + 1), alpha=0.7, color='green', 
                edgecolor='black', linewidth=0.5)
        
        plt.axvline(x=mc_results['velocity_p10'], color='green', linestyle='--', linewidth=2, label='P10')
        plt.axvline(x=mc_results['velocity_p50'], color='orange', linestyle='--', linewidth=2, label='P50')
        plt.axvline(x=mc_results['velocity_p90'], color='red', linestyle='--', linewidth=2, label='P90')
        
        plt.title("📊 Distribuição de Velocidade da Organização", fontsize=14, pad=20)
        plt.xlabel("Velocidade (issues/semana)", fontsize=12)
        plt.ylabel("Frequência", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.savefig(vel_filename)
        plt.close()
        
        return mc_filename, vel_filename

    def create_monte_carlo_explanation(self, mc_results: dict) -> str:
        """Create explanation for Monte Carlo simulation results."""
        markdown = "### Explicação da Simulação Monte Carlo\n\n"
        markdown += "| Conceito | Explicação |\n"
        markdown += "|---------|------------|\n"
        markdown += "| **O que é Monte Carlo?** | Técnica estatística que utiliza amostragens aleatórias repetidas para obter resultados numéricos e estimar probabilidades. |\n"
        markdown += "| **Como funciona a simulação?** | 1) Coletamos o histórico de velocidade da organização (issues concluídas/semana)<br>2) Fazemos 1000 simulações com variações aleatórias dessas velocidades<br>3) Para cada simulação, calculamos quando o trabalho restante seria concluído<br>4) Organizamos os resultados e calculamos os percentis |\n"
        markdown += "| **O que significa P10?** | Cenário otimista. Existe apenas 10% de chance de concluir o trabalho antes desta data. É um resultado rápido e favorável, mas menos provável. |\n"
        markdown += "| **O que significa P50?** | Cenário mais provável. 50% de chance de terminar antes ou depois desta data. É nossa melhor estimativa 'realista'. |\n"
        markdown += "| **O que significa P90?** | Cenário conservador. Existe 90% de chance de concluir antes desta data. Útil para planejamento seguro, pois é improvável atrasar além deste ponto. |\n"
        markdown += "| **Por que usar Monte Carlo?** | Fornece intervalos de confiança em vez de datas únicas, reconhecendo a incerteza natural no desenvolvimento. Captura a variabilidade histórica da organização. |\n"
        markdown += "| **Como interpretar velocidades?** | Quanto maior a velocidade, mais rápido a organização conclui issues. P10/P50/P90 para velocidades mostram diferentes cenários de produtividade que usamos nos cálculos. |\n"
        
        # Add data context if we have simulation data
        if mc_results['simulation_data'] and len(mc_results['simulation_data']) > 0:
            historical_context = "| **Contexto dos dados** | "
            
            if mc_results['completion_date_p10'] != "Complete" and mc_results['completion_date_p10'] is not None:
                # Extract velocity info for volatility calculation
                historical_velocities = []
                for sim in mc_results['simulation_data']:
                    if 'velocity' in sim:
                        historical_velocities.append(sim['velocity'])
                
                # Calculate and interpret volatility
                if historical_velocities:
                    mean_velocity = np.mean(historical_velocities)
                    std_velocity = np.std(historical_velocities)
                    volatility = (std_velocity / mean_velocity) * 100 if mean_velocity > 0 else 0
                    
                    if volatility < 20:
                        volatility_desc = "baixa volatilidade (organização consistente)"
                    elif volatility < 40:
                        volatility_desc = "volatilidade moderada (alguma variação na entrega)"
                    else:
                        volatility_desc = "alta volatilidade (entregas inconsistentes)"
                    
                    # Calculate spread between scenarios
                    if mc_results['completion_date_p10'] and mc_results['completion_date_p90']:
                        p10_date = pd.to_datetime(mc_results['completion_date_p10'])
                        p90_date = pd.to_datetime(mc_results['completion_date_p90'])
                        delta_days = (p90_date - p10_date).days
                        
                        historical_context += f"Com base nos dados históricos, a organização tem {volatility_desc}. "
                        historical_context += f"A diferença entre o cenário otimista e conservador é de {delta_days} dias. "
                        
                        # Add recommendation based on data quality
                        if volatility < 30:
                            historical_context += f"Os dados são confiáveis para planejamento. Recomendamos usar P50 ({mc_results['completion_date_p50']}) para comunicação de prazos."
                        else:
                            historical_context += f"Devido à alta variabilidade, considere usar P70-P80 para comunicação de prazos ao invés de P50."
            
            historical_context += " |"
            markdown += historical_context + "\n"
        
        return markdown

    def generate_markdown_report(self, stats: dict, weekly_data: pd.DataFrame, mc_results: dict) -> str:
        """Generate complete markdown report for the organization."""
        # Limitar aos últimos 6 meses
        now = datetime.now()
        six_months_ago = now - pd.DateOffset(months=6)
        filtered_weekly = weekly_data[weekly_data["period"] >= six_months_ago]

        # Start with the header and summary stats
        markdown = self.generate_markdown_header(stats)
        markdown += "\n---\n"
        
        # Add biweekly delivery section
        weekly_file = self.plot_weekly_delivery(filtered_weekly)
        markdown += "## 📊 Entregas Quinzenais da Organização\n\n"
        markdown += f"![Organization biweekly chart]({weekly_file})\n\n"
        
        # Add velocity stats
        avg_velocity = filtered_weekly["delivered"].mean().round(2)
        markdown += f"**Velocidade média quinzenal:** {avg_velocity} issues/quinzena\n\n"
        
        # Add biweekly data table
        markdown += "| Período | Prometido | Entregue | % Concluído | Velocidade |\n"
        markdown += "|--------|------------|----------|--------------|------------|\n"
        
        for _, row in filtered_weekly.sort_values("period").iterrows():
            period = row['period'].strftime('%Y-%m-%d')
            markdown += f"| {period} | {int(row['promised'])} | {int(row['delivered'])} | {round(row['percent_completed'], 1)}% | {int(row['delivered'])} |\n"
        
        markdown += "\n"
        
        # Add burnup chart section
        burnup_file, _ = self.plot_burnup_chart(filtered_weekly)
        markdown += "## 🔥 Burn-up Chart da Organização\n\n"
        markdown += f"![Organization burnup chart]({burnup_file})\n\n"
        
        # Add Monte Carlo section if we have simulation data
        if mc_results and mc_results['simulation_data']:
            mc_file, vel_file = self.plot_monte_carlo_simulations(mc_results)
            
            markdown += "## 🎲 Simulação Monte Carlo\n\n"
            markdown += f"![Organization monte carlo simulation]({mc_file})\n\n"
            markdown += f"![Organization velocity distribution]({vel_file})\n\n"
            
            # Add results table
            markdown += "### Previsões de Velocidade e Conclusão da Organização\n\n"
            markdown += "| Métrica | Valor |\n"
            markdown += "|--------|-------|\n"
            
            markdown += f"| Velocidade Média | {mc_results['velocity_mean']:.2f} issues/quinzena |\n"
            markdown += f"| Velocidade P10 (Otimista) | {mc_results['velocity_p10']:.2f} issues/quinzena |\n"
            markdown += f"| Velocidade P50 (Provável) | {mc_results['velocity_p50']:.2f} issues/quinzena |\n"
            markdown += f"| Velocidade P90 (Conservador) | {mc_results['velocity_p90']:.2f} issues/quinzena |\n"
            
            if mc_results['completion_date_p10'] == "Complete":
                markdown += f"| Conclusão | Já concluído |\n"
            elif mc_results['completion_date_p10'] is None:
                markdown += f"| Conclusão | Dados insuficientes para previsão |\n"
            else:
                markdown += f"| Data de Conclusão P10 (Otimista) | {mc_results['completion_date_p10']} |\n"
                markdown += f"| Data de Conclusão P50 (Provável) | {mc_results['completion_date_p50']} |\n"
                markdown += f"| Data de Conclusão P90 (Conservador) | {mc_results['completion_date_p90']} |\n"
            
            markdown += "\n"
            
            # Add Monte Carlo explanation
            markdown += self.create_monte_carlo_explanation(mc_results)
        
        return markdown
    def run_monte_carlo_simulation(self, weekly_data: pd.DataFrame) -> dict:
        """Run Monte Carlo simulation for organization completion date."""
        # Sort data chronologically
        df = weekly_data.sort_values("period")
        
        # Extract historical velocities
        velocities = df["delivered"].tolist()
        
        # Calculate remaining work
        df["cumulative_promised"] = df["promised"].cumsum()
        df["cumulative_delivered"] = df["delivered"].cumsum()
        remaining_work = df["cumulative_promised"].max() - df["cumulative_delivered"].max()
        
        # If no work left, return completed status
        if remaining_work <= 0:
            return {
                'velocity_mean': np.mean(velocities),
                'velocity_p10': np.percentile(velocities, 10) if len(velocities) > 0 else 0,
                'velocity_p50': np.percentile(velocities, 50) if len(velocities) > 0 else 0,
                'velocity_p90': np.percentile(velocities, 90) if len(velocities) > 0 else 0,
                'completion_date_p10': "Complete",
                'completion_date_p50': "Complete",
                'completion_date_p90': "Complete",
                'simulation_data': [],
            }
        
        # Get last date as starting point
        last_date = pd.to_datetime(df["period"].max())
        
        # Run simulations
        simulation_data = []
        print(f"🎲 Executando {self.monte_carlo_simulations} simulações Monte Carlo...")
        
        for _ in range(self.monte_carlo_simulations):
            # Bootstrap sampling of historical velocities
            sampled_velocities = random.choices(velocities, k=len(velocities))
            
            # Calculate mean velocity with random factor
            mean_velocity = np.mean(sampled_velocities) * random.uniform(0.8, 1.2)
            
            # Skip if velocity is zero or negative
            if mean_velocity <= 0:
                continue
            
            # Calculate periods to completion
            periods_to_completion = remaining_work / mean_velocity
            
            # Calculate completion date - now each period is 14 days (biweekly)
            completion_date = last_date + pd.Timedelta(days=int(periods_to_completion * 14))
            
            # Store simulation results
            simulation_data.append({
                'velocity': mean_velocity,
                'periods_to_completion': periods_to_completion,
                'completion_date': completion_date
            })
        
        # Calculate statistics from simulation results
        if not simulation_data:
            return {
                'velocity_mean': np.mean(velocities) if velocities else 0,
                'velocity_p10': 0, 
                'velocity_p50': 0,
                'velocity_p90': 0,
                'completion_date_p10': None,
                'completion_date_p50': None,
                'completion_date_p90': None,
                'simulation_data': [],
            }
        
        # Extract velocities and completion dates
        all_velocities = [sim['velocity'] for sim in simulation_data]
        all_completion_dates = [sim['completion_date'] for sim in simulation_data]
        
        # Calculate percentiles
        velocity_mean = np.mean(all_velocities)
        velocity_p10 = np.percentile(all_velocities, 10)
        velocity_p50 = np.percentile(all_velocities, 50)
        velocity_p90 = np.percentile(all_velocities, 90)
        
        # Calculate date percentiles
        completion_dates_sorted = sorted(all_completion_dates)
        idx_p10 = min(int(0.1 * len(completion_dates_sorted)), len(completion_dates_sorted) - 1)
        idx_p50 = min(int(0.5 * len(completion_dates_sorted)), len(completion_dates_sorted) - 1)
        idx_p90 = min(int(0.9 * len(completion_dates_sorted)), len(completion_dates_sorted) - 1)
        
        completion_date_p10 = completion_dates_sorted[idx_p10]
        completion_date_p50 = completion_dates_sorted[idx_p50]
        completion_date_p90 = completion_dates_sorted[idx_p90]
        
        print("✅ Simulações Monte Carlo concluídas.")
        
        return {
            'velocity_mean': velocity_mean,
            'velocity_p10': velocity_p10,
            'velocity_p50': velocity_p50,
            'velocity_p90': velocity_p90,
            'completion_date_p10': completion_date_p10.strftime('%Y-%m-%d'),
            'completion_date_p50': completion_date_p50.strftime('%Y-%m-%d'),
            'completion_date_p90': completion_date_p90.strftime('%Y-%m-%d'),
            'simulation_data': simulation_data,
        }





    def run(self):
        # Compute overall stats
        stats = self.compute_stats()
        print(f"📊 Estatísticas calculadas: {stats['total']} issues totais, {stats['percent_closed']}% concluídas.")
        
        # Compute weekly stats
        weekly_data = self.compute_weekly_delivery_stats()
        print(f"📅 Dados semanais processados para {len(weekly_data)} semanas.")
        
        # Run Monte Carlo simulation
        mc_results = self.run_monte_carlo_simulation(weekly_data)
        
        # Generate markdown report
        markdown = self.generate_markdown_report(stats, weekly_data, mc_results)
        if self.save_func is None:
            raise ValueError("Função de salvamento não definida. Por favor, forneça uma função de salvamento válida.")
        self.save_func(self.report_dir, "organization_stats.md", markdown)
        print("📄 Relatório gerado com sucesso: organization_stats.md")
        
        
        