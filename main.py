import os
from datetime import datetime

def logger_with_params(path):

    def logger(old_function):
        
        def new_function(*arguments, **keyword_args):
            result_old_func = old_function(*arguments, **keyword_args)

            with open(path, "a", encoding="UTF-8") as log_file:
                log_file.write("Дата, время: " + str(datetime.now()) + "\n")
                log_file.write("Имя функции: " + old_function.__name__ + "\n")

                args = ''
                for arg in arguments:
                    args += str(arg) + ', '
                log_file.write("Позиционные агрументы: " + args.rstrip(", ") + "\n")

                kwargs = ''
                for key, value in keyword_args.items():
                    kwargs += key + ' = ' + str(value) + ', '
                log_file.write("Именнованные аргументы: " + kwargs.rstrip(", ") + "\n")

                log_file.write("Результат функции: " + str(result_old_func) + "\n\n")

            return result_old_func
        
        return new_function
    
    return logger

def main():
    
    paths = ('log_1.log', 'log_2.log', 'log_3.log')
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        log_decorator = logger_with_params(path)

        @log_decorator
        def hello_world() -> str:
            return 'Hello World'
        
        @log_decorator
        def summator(a, b=0) -> int:
            return a + b
        
        @log_decorator
        def div(a, b) -> float:
            return a / b

        assert 'Hello World' == hello_world()

        result = summator(2, 2)
        assert isinstance(result, int)
        assert result == 4

        result = div(6, 2)
        assert result == 3

        summator(4.3, b=2.2)
        summator(a=0, b=0)

        assert os.path.exists(path)

        with open(path, "r", encoding="UTF-8") as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content
        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content

if __name__ == '__main__':
    main()