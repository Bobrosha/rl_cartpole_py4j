package ru.dutov.cartpole.main;

import ru.dutov.cartpole.env.CartPoleEnv;

public class Main {
    public static void main(String[] args) {
        CartPoleEnv env = new CartPoleEnv();
        env.Start();
    }
}
