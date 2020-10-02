package ru.dutov.cartpole.env;

public class Status {
    private double x;
    private double xDot;
    private double theta;
    private double thetaDot;
    private float reward;
    private boolean done;

    public double getX() { return x; }

    public double getXDot() {
        return xDot;
    }

    public double getTheta() {
        return theta;
    }

    public double getThetaDot() {
        return thetaDot;
    }

    public float getReward() {
        return reward;
    }

    public boolean isDone() {
        return done;
    }

    public Status(double x, double xDot, double theta, double thetaDot, float reward, boolean done) {
        this.x = x;
        this.xDot = xDot;
        this.theta = theta;
        this.thetaDot = thetaDot;
        this.reward = reward;
        this.done = done;
    }

    public void reset() {
        double min = -0.05;
        double max = 0.05;

        this.x = Math.random() * (max-min) + min;
        this.xDot = Math.random() * (max-min) + min;
        this.theta = Math.random() * (max-min) + min;
        this.thetaDot = Math.random() * (max-min) + min;
        this.reward = 0;
        this.done = false;
    }

    /*public void print() {
        System.out.format("%n" + "%f; %f; %f; %f" + "%n", this.x, this.xDot, this.theta, this.thetaDot);
        System.out.print("Reward: ");
        System.out.println(this.reward);
        System.out.print("Done: ");
        System.out.println(this.done);
    }*/ // Use only for tests
}



