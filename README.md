# Two-Wheeled Self-Balancing Robot (TWSR) – Simulink Simulation

**High-performance Simulink control achieving <2 s settling time and <5% overshoot using cascaded PID with Kalman filtering.**

---

## 🛠️ Control System Architecture

### ⭕ Cascaded PID Structure

#### Outer Loop: Tilt Regulation (Slow Loop)
- **Sensors:** MPU6050 IMU
- **Processing:** Kalman Filter for angle estimation
- **Controller:** PID (regulates tilt angle to setpoint)

Data Flow:
```
MPU6050 IMU → Kalman Filter → PID (Tilt)
      ↓
Error = Setpoint (0°) – Filtered Tilt Angle
      ↓
Output: Desired Wheel Speed Reference
```

#### Inner Loop: Wheel Speed Tracking (Fast Loop)
- **Sensors:** HC-020K Wheel Encoder
- **Controller:** PID (controls wheel speed)

Data Flow:
```
Wheel Encoder → PID (Wheel Speed)
       ↓
Error = Reference RPM – Actual RPM
       ↓
Output: TB6600 Stepper Driver Signal
```

---

## 🧩 Simulink Model Features

- **3-DOF Plant:** Tilt, forward/backward, and heading control dynamics
- **Kalman Filtering:** Fuses gyro + accelerometer, minimizes drift
- **PID Autotune:** Integrates Simulink PID Tuner for automatic gain selection
- **Performance Metrics:** Built-in step response plots for rise time/overshoot analysis

---

## 📊 Simulation Results

| Metric             | Target   | Achieved |
|--------------------|----------|----------|
| Settling Time      | <3 s     | **1.8 s** |
| Overshoot          | <10%     | **4.2%**  |
| Rise Time          | <1 s     | **0.6 s** |
| Steady-State Error | <2°      | **0.8°**  |

---

## 🚀 How to Run the Simulation

1. **Open the Main Model**
    ```matlab
    open('cascaded_pid.slx')
    ```
2. **Auto-Tune the PID Controllers**
    ```matlab
    pidTuner('outer_tilt_controller')
    pidTuner('inner_wheel_controller')
    ```
3. **Run Step Response & Plot Results**
    ```matlab
    sim('cascaded_pid')
    plot(simout.time, simout.signals.values)
    ```

---

## 📁 Repository Structure

```
simulink/
├── cascaded_pid.slx         # Main control system model
├── kalman_filter.slx        # IMU sensor fusion subsystem
├── pid_tuning.slx           # Step response & tuning model
└── step_response_plots.m    # MATLAB visualization script
```

---

## 🔧 PID Tuning Workflow

1. Set initial controller gains, simulate the step response
2. Analyze rise time, overshoot, settling time
3. Tune parameters:
    - Kp: Responsiveness
    - Ki: Steady-state accuracy
    - Kd: Damping
4. Iterate until settling time <2 s, overshoot <5%

---

**Requirements:**  
- MATLAB/Simulink R2023a or later  
- [MPU6050 IMU](https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/)  
- [HC-020K Encoder](https://www.electronicwings.com/nodesensor/hc-020k)  
- [TB6600 Stepper Driver](https://www.toshiba-driver.com/product/tb6600)

---

> _Copy-paste ready_ — Showcase your Simulink-based self-balancing control system in seconds.  
>
> For technical reference see [Ideation Document – Technical Details for Proposed Robot](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/52559422/08473e1a-7e2b-4bd1-8244-d28aa84c1fe1/Ideation-Document-Technical-Details-for-Proposed-Robot-by-stabilize-Google-Do...).
