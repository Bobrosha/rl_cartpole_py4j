# rl_cartpole_py4j

Обучение нейронной сети tensorflow keras на модели cartpole джава, с использованием фреймворка py4j.

Программа на java https://github.com/Bobrosha/rl_cartpole_py4j/tree/master/src/main/java/ru/dutov/cartpole
Реализует модель cartpole и запускает шлюз, для доступа нейронной сети к модели.

Программа на Python "agent_client.py".
Реализует агента и необходимые для него условия.

Запускать обязательно вначале код java, затем код python. Начнется обучение модели на 500 эпизодах.
После окончания обучения не забудьте остановить выполнение java кода.
