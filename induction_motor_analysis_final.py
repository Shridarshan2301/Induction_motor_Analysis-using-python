import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import math as mth

class Motor:
    """A base class for electric motors."""
    def __init__(self, frequency, poles, voltage, current, pf=0.85):
        self.frequency = frequency
        self.poles = poles
        self.voltage = voltage
        self.current = current
        self.pf = pf

    @property
    def synchronous_speed(self):
        """Calculates the synchronous speed in RPM."""
        if self.poles == 0:
            return 0
        return 120 * self.frequency / self.poles

    @property
    def input_power(self):
        """Calculates the input power in Watts."""
        return np.sqrt(3) * self.voltage * self.current * self.pf

class InductionMotor(Motor):
    """Represents an induction motor, inheriting from the base Motor class."""
    def __init__(self, frequency, poles, voltage, current, rotor_speed,
                 r1, x1, r2, x2, t_ratio, pf):
        super().__init__(frequency, poles, voltage, current, pf)
        self.rotor_speed = rotor_speed
        self.r1 = r1
        self.x1 = x1
        self.r2 = r2
        self.x2 = x2
        self.tr = t_ratio

    @property
    def slip(self):
        """Calculates the slip of the motor."""
        Ns = self.synchronous_speed
        if Ns == 0:
            return 0
        return (Ns - self.rotor_speed) / Ns

    @property
    def torque(self):
        """Calculates the output torque in Nm."""
        s = self.slip
        n = self.synchronous_speed
        r2 = self.r2
        x2 = self.x2
        e2 = self.voltage * self.tr
        
        denominator = 2 * mth.pi * n * ((r2)**2 + (x2 * s)**2)
        if denominator == 0:
            return 0
            
        tor = (60 * e2**2 * r2 * s) / denominator
        return tor

    @property
    def output_power(self):
        """Calculates the output power in Watts."""
        return 2 * mth.pi * self.rotor_speed * self.torque / 60

    @property
    def efficiency(self):
        """Calculates the efficiency of the motor in percent."""
        input_pow = self.input_power
        output_pow = self.output_power

        if input_pow <= 0 or output_pow < 0:
            return 0

        eff = (output_pow / input_pow) * 100
        return min(eff, 100) # Efficiency cannot exceed 100%

    def get_report(self):
        """Generates a formatted string with the motor's performance details."""
        return (
            "Induction Motor Performance Report\n"
            "------------------------------------\n"
            f"Synchronous Speed: {self.synchronous_speed:.2f} RPM\n"
            f"Rotor Speed: {self.rotor_speed:.2f} RPM\n"
            f"Slip: {self.slip * 100:.2f} %\n"
            f"Torque: {self.torque:.2f} Nm\n"
            f"Output Power: {self.output_power / 1000:.2f} kW\n"
            f"Efficiency: {self.efficiency:.2f} %"
        )

class MotorClassifier:
    """Classifies motor performance based on slip and speed."""
    def __init__(self, motor):
        self.motor = motor

    def classify_slip(self):
        s = self.motor.slip
        if s < 0:
            return "Generator mode (negative slip)"
        elif s < 0.03:
            return "High-efficiency, low-load zone"
        elif s < 0.06:
            return "Moderate efficiency, rated load zone"
        else:
            return "Low-efficiency, overloaded zone"

    def classify_speed(self):
        Ns = self.motor.synchronous_speed
        Nr = self.motor.rotor_speed
        if Ns == 0:
            return "Cannot classify (Synchronous speed is zero)"
        if Nr >= 0.95 * Ns:
            return "Near-synchronous operation"
        elif Nr >= 0.9 * Ns:
            return "Normal operating speed"
        else:
            return "Low speed, potentially overloaded"
            
    def get_report(self):
        
        return (
            "\nClassification Results\n"
            "------------------------\n"
            f"Slip-based classification: {self.classify_slip()}\n"
            f"Speed-based classification: {self.classify_speed()}"
        )


class MotorPlotter:
    """Handles the generation of performance plots for a motor."""
    def __init__(self, motor):
        self.motor = motor

    def plot_torque_speed(self):
        original_speed = self.motor.rotor_speed
        rotor_speeds = np.linspace(0, self.motor.synchronous_speed, 100)
        torques = []
        for n in rotor_speeds:
            self.motor.rotor_speed = n
            torques.append(self.motor.torque)

        self.motor.rotor_speed = original_speed
        
        plt.figure(figsize=(8,5))
        plt.plot(rotor_speeds, torques, color="blue", linewidth=2)
        plt.title("Torque-Speed Characteristic")
        plt.xlabel("Rotor Speed (RPM)")
        plt.ylabel("Torque (Nm)")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()

    def plot_slip_speed(self):
        original_speed = self.motor.rotor_speed
        rotor_speeds = np.linspace(0, self.motor.synchronous_speed, 100)
        slips = []
        for n in rotor_speeds:
            self.motor.rotor_speed = n
            slips.append(self.motor.slip * 100)

        self.motor.rotor_speed = original_speed

        df = pd.DataFrame({"Rotor Speed": rotor_speeds, "Slip (%)": slips})
        sns.lineplot(x="Rotor Speed", y="Slip (%)", data=df, color="green")
        plt.title("Slip vs. Rotor Speed")
        plt.xlabel("Rotor Speed (RPM)")
        plt.ylabel("Slip (%)")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()
    
    def plot_efficiency_vs_output_power(self):
        original_speed = self.motor.rotor_speed
        rotor_speeds = np.linspace(0.5 * self.motor.synchronous_speed, 
                                   0.999 * self.motor.synchronous_speed, 100)
        efficiencies = []
        output_powers = []
        
        for n in rotor_speeds:
            self.motor.rotor_speed = n
            efficiencies.append(self.motor.efficiency)
            output_powers.append(self.motor.output_power)
        
        self.motor.rotor_speed = original_speed
        
        plt.figure(figsize=(8,5))
        plt.plot(output_powers, efficiencies, color="purple", linewidth=2)
        plt.title("Efficiency vs. Output Power")
        plt.xlabel("Output Power (W)")
        plt.ylabel("Efficiency (%)")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()


def main():
    
    print('Enter the Induction motor parameters')
    try:
        f = float(input("Enter Frequency (Hz): "))
        p = int(input("Enter No. of Poles: "))
        v = float(input("Enter Voltage (V): "))
        i = float(input("Enter Current (A): "))
        n = float(input("Enter Rotor Speed (RPM): "))
        r1 = float(input("Enter stator resistance (Ohm): "))
        x1 = float(input("Enter stator reactance (Ohm): "))
        r2 = float(input("Enter rotor resistance (Ohm): "))
        x2 = float(input("Enter rotor reactance (Ohm): "))
        t = float(input("Enter transformation ratio (rotor/stator): "))
        pf = float(input("Enter input power factor (e.g., 0.85): "))

        if f <= 0 or p <= 0 or v <= 0 or i <= 0 or n < 0 or pf <= 0 or pf > 1:
            raise ValueError("Input values must be positive. Power factor must be between 0 and 1.")
    
        motor = InductionMotor(f, p, v, i, n, r1, x1, r2, x2, t, pf)
        classifier = MotorClassifier(motor)

       
        motor_report_str = motor.get_report()
        classifier_report_str = classifier.get_report()

       
        print("\n" + motor_report_str)
        print(classifier_report_str)

        
        try:
            with open("report.txt", "w") as report_file:
                report_file.write("--- Detailed Induction Motor Analysis Report ---\n\n")
                report_file.write("--- Input Parameters ---\n")
                report_file.write(f"Frequency: {f} Hz\n")
                report_file.write(f"Poles: {p}\n")
                report_file.write(f"Voltage: {v} V\n")
                report_file.write(f"Current: {i} A\n")
                report_file.write(f"Rotor Speed: {n} RPM\n")
                report_file.write(f"Stator Resistance: {r1} Ohm\n")
                report_file.write(f"Stator Reactance: {x1} Ohm\n")
                report_file.write(f"Rotor Resistance: {r2} Ohm\n")
                report_file.write(f"Rotor Reactance: {x2} Ohm\n")
                report_file.write(f"Transformation Ratio: {t}\n")
                report_file.write(f"Power Factor: {pf}\n\n")
                
                report_file.write(motor_report_str + "\n")
                report_file.write(classifier_report_str + "\n")
            print("\n[Success] Detailed report was saved to 'report.txt'.")
        except IOError as e:
            print(f"\n[File Error] Could not write the report to 'report.txt'. Reason: {e}")

        
        print("\nGenerating performance plots...")
        plotter = MotorPlotter(motor)
        plotter.plot_torque_speed()
        plotter.plot_slip_speed()
        plotter.plot_efficiency_vs_output_power()
        
    except ValueError as e:
        print(f"\n[Input Error] Invalid input. Please enter valid numbers. Details: {e}")
    except Exception as e:
        print(f"\n[An Unexpected Error Occurred] Details: {e}")

if __name__ == "__main__":
    main()