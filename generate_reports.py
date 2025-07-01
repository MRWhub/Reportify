
if __name__ == "__main__":
    from src.reportify.view.generate_all import CreateAllReports
    from src.reportify.send_discord import SendDiscordSummaries
    CreateAllReports()
    SendDiscordSummaries()