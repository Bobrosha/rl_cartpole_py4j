package ru.dutov.cartpole.env;

import py4j.GatewayServer;

/**
 * Класс реализующий окружение (тележку)
 *
 * Все параметры в этом классе используются только внутри для расчетов положения тележки
 */
public class CartPoleEnv {
    /**
     * @param state единственная переменная, которая возвращается и передает статус тележки
     */
    private double pi;

    private double gravity;
    private final double masspole;
    private double totalMass;
    private double length;
    private final double polemassLength;
    private double forceMag;
    private double tau;

    private double thetaThresholdRadians;
    private double xThreshold;

    private int actionSpace;
    private int observationSpace;

    public int getObservationSpace() {
        return observationSpace;
    }

    public int getActionSpace() {
        return actionSpace;
    }

    private Status state = new Status(1, 1, 1, 1, 1, true);

    private GatewayServer server = new GatewayServer();

    /**
     * Метод запускающий сервер для связи с Python
     */
    public void Start() {
        server.start(true);
    }

    public CartPoleEnv() {
        double masscart = 1.0d;

        this.pi = Math.PI;

        this.gravity = 9.8d;
        this.masspole = 0.1d;
        this.totalMass = masspole + masscart;
        this.length = 0.5d;
        this.polemassLength = masspole * length;
        this.forceMag = 10.0d;
        this.tau = 0.02d;

        this.thetaThresholdRadians = 12 * 2 * pi / 360;
        this.xThreshold = 2.4d;

        this.actionSpace = 2;
        this.observationSpace = 4;
    }

    /**
     * Метод обновляющий состояние тележки
     * @param action совершенное действие
     * @return обновленное состояние
     */
    public Status step(int action) {
        double x = this.state.getX();
        double xDot = this.state.getXDot();
        double theta = this.state.getTheta();
        double thetaDot = this.state.getThetaDot();

        double force = action == 1 ? this.forceMag : -this.forceMag;
        double costheta = Math.cos(theta);
        double sintheta = Math.sin(theta);

        double tmp = (force + this.polemassLength * thetaDot * thetaDot * sintheta) / this.totalMass;
        double thetaacc = (this.gravity * sintheta - costheta * tmp) / (this.length * (4.0 / 3.0 - this.masspole * costheta * costheta / this.totalMass));
        double xacc = tmp - this.polemassLength * thetaacc * costheta / this.totalMass;

        x += this.tau * xDot;
        xDot += this.tau * xacc;
        theta += this.tau * thetaDot;
        thetaDot += this.tau * thetaacc;

        boolean done = false;
        if (x < -this.xThreshold || x > this.xThreshold || theta < -this.thetaThresholdRadians || theta > this.thetaThresholdRadians) {
            done = true;
        }

        int reward = done ? 0 : 1;

        this.state = new Status(x, xDot, theta, thetaDot, reward, done);

        return this.state;
    }

    /**
     * Метод сбрасывающий состояние тележки к начальному
     * @return Возвращает состояние тележки
     */
    public Status reset() {
        this.state.reset();
        return this.state;
    }
}