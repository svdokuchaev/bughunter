import bot
from multiprocessing import Process


class BotRunner(bot.Bot):
    """Управляет запуском ботов"""

    def run(self):
        self.setup()
        count = self.elements.top_item.count_elements()
        assert count > 1, "Проблемы с загрузкой панели навигации"
        for i in range(1):  # count
            Process(target=bot.run_bot, args=(i,)).start()

if __name__ == '__main__':
    bot_runner = BotRunner(1)
    bot_runner.run()