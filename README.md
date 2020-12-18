# rl_cartpole_py4j

Обучение нейронной сети tensorflow keras на модели cartpole джава, с использованием фреймворка py4j.<br><br>

java модель https://github.com/Bobrosha/rl_cartpole_py4j/tree/master/src/main/java/ru/dutov/cartpole<br>
Реализует модель cartpole и запускает шлюз, для доступа нейронной сети к модели.<br>

Программа на Python "agent_client.py".<br>
Реализует агента и необходимые для него условия.<br>

Запускать обязательно вначале код java, затем код python. Начнется обучение модели на 500 эпизодах.<br>
После окончания обучения не забудьте остановить выполнение java кода.<br>
