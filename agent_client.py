import numpy as np
from collections import deque
from tensorflow import keras
from tensorflow.keras import regularizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import random
from py4j.java_gateway import JavaGateway

class Agent():
    # Инициализация
    def __init__(self, observ_space, action_space):
        self.observ_size = observ_space # Количество параметров входящих в нейронную сеть
        self.action_size = action_space # Количество вариантов действий агента
        self.memory = deque(maxlen = 2000) # Хранилище совершенных агентом действий и их последствий
        self.gamma = 0.95 # Фактор дисконтирования. Коэффициент уменьшения вознаграждения
        
        self.freeroll_rate = 1.0 # Процент рандомных действий агента
        self.freeroll_min = 0.01 # Минимальный процент
        self.freeroll_decay = 0.995 # Уменьшение рандомных решений после каждого обучения
        self.learning_rate = 0.001 # Изменение скорости обучения оптимизатора с течением времени
        self.model = self.build_model() # Модель
    
    # Создание скомпилированной модели
    def build_model(self):
        model = Sequential()
        
        model.add(Dense(24, activation='relu', input_dim=self.observ_size))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', 
                      optimizer=Adam(lr = self.learning_rate))
        return model
        
    # Сохранение истории в очередь
    def remember(self, state, action, reward, state_next, done):
        self.memory.append((state, action, reward, state_next, done))
    
    # Определяет и возвращает действие
    def get_action(self, state):
        # Случайный выбор действия
        if np.random.rand() <= self.freeroll_rate: 
            return self.get_random_action()
        
        # Использование предсказания агента для выбора действия
        test = self.model.predict(state)
        return np.argmax(test[0]).item() # Возвращает действие
    
    def get_random_action(self):
        return random.randrange(self.action_size)
    
    # Обучение
    def training(self, batch_size):        
        if len(self.memory) < batch_size: return
        # Случайная выборка batch_size элементов для обучения агента
        sample_batch = random.sample(self.memory, batch_size)
        for state, action, reward, state_next, done in sample_batch:
            q_values = self.model.predict(state)
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(state_next)[0])
            # Формируем цель обучения сети
            q_values[0][action] = target
            # Обучение сети
            self.model.fit(state, q_values, verbose=0)
        if self.freeroll_rate > self.freeroll_min: 
            self.freeroll_rate *= self.freeroll_decay
            
if __name__ == "__main__":
    def get_state(java_state):
        done = java_state.isDone()
        reward = java_state.getReward()
        state = np.array([[java_state.getX(), java_state.getXDot(), java_state.getTheta(), java_state.getThetaDot()]], dtype = np.float64)
        return state, done, reward
    
    # DQN - глубокая Q-нейронная сеть
    java_gateway = JavaGateway()
    env = java_gateway.jvm.ru.dutov.cartpole.env.CartPoleEnv()
    
    observ_space = env.getObservationSpace()
    action_space = env.getActionSpace()
    
    agent = Agent(observ_space, action_space) # Создаем агента
    
    episodes = 500 # Число игровых эпизодов
    
    scores = deque(maxlen = 100)
    # scores - хранит длительность последних 100 игр

    #
    # Цикл игры и обучения
    #

    for e in range(episodes + 1):
        # Получаем начальное состояние объекта перед началом каждого эпизода
        state, done, reward = get_state(env.reset())        
        
        # frame - текущий кадр (момент) игры
        frames = 0
        
        while not done:            
            frames += 1
            action = agent.get_action(state) # Определяем очередное действие
            
            state_next, done, reward = get_state(env.step(action))

            # Получаем от среды обновленные состояние объекта, награду, значение флага завершения игры
            # В каждый момент игры, пока не наступило одно из условий ее прекращения, награда равна 1
            
            agent.remember(state, action, reward, state_next, done)
            # Запоминаем предыдущее состояние объекта, действие, 
            # награду за это действие, текущее состояние, значение done
            
            state = state_next # Обновляем текущее состояние
            
        print("Эпизод: {:>3}/{}, продолжительность игры в кадрах: {:>3}".format(e, episodes, frames))
        
        scores.append(frames)
        score_mean = np.mean(scores)
        
        if score_mean >= 195:
            print('Цель достигнута. Средняя продолжительность игры: ', score_mean)
            failFlag = False
            break
            
        print('Средняя продолжительность: ', score_mean, '\n')
        
        # Продолжаем обучать агента
        agent.training(32)
        
        # Если эпизоды закончились, а средняя продолжительность последних 100 игры < 195,
        # то задача считается не решенной
