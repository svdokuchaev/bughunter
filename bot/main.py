import bot
import subprocess
import time


class BotRunner(bot.Bot):
    """Управляет запуском ботов"""

    def run(self):
        self.setup()
        count = self.elements.top_item.count_elements()
        assert count > 1, "Проблемы с загрузкой панели навигации"
        process = []
        for i in range(1, 6):  # count
            p = subprocess.Popen(["python", "bot.py", str(i)])
            process.append(p)
            time.sleep(0.2)
        while [1 for p in process if p.poll() is None]:
            time.sleep(5)


if __name__ == '__main__':
    bot_runner = BotRunner(None)
    bot_runner.run()
    bot_runner.kill()