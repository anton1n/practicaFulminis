#!/usr/bin/env python3

from pymodbus.client import ModbusTcpClient
import time
import sys

class ATV630Controller:
    def __init__(self, ip_address='192.168.100.125', port=502, unit_id=1):
        self.ip = ip_address
        self.port = port
        self.unit_id = unit_id
        self.client = None
        
        self.COMMAND_WORD = 8501      # CMD register
        self.FREQ_REFERENCE = 8502    # Frequency setpoint
        self.STATUS_WORD = 3201       # Status register
        self.ACTUAL_FREQ = 3202       # Actual frequency
        self.MOTOR_CURRENT = 3204     # Motor current
        
        # Command values
        self.CMD_STOP = 0x0006
        self.CMD_START_FWD = 0x000F
        self.CMD_START_REV = 0x0007
        self.CMD_EMERGENCY_STOP = 0x0000
        self.CMD_RESET_FAULT = 0x0080
        self.CMD_ENABLE_RUN_FWD = 0x047F
    
    def connect(self):
        try:
            self.client = ModbusTcpClient(self.ip, port=self.port)
            self.client.unit_id = self.unit_id
            
            if self.client.connect():
                print(f"Connected to ATV630 at {self.ip}:{self.port}")
                return True
            else:
                print(f"Failed to connect to {self.ip}:{self.port}")
                return False
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        if self.client:
            self.client.close()
            print("Disconnected from ATV630")
    
    def read_status(self):
        try:
            result = self.client.read_holding_registers(self.STATUS_WORD)
            if hasattr(result, 'registers') and result.registers:
                status = result.registers[0]
                
                print(f"\n=== Drive Status ===")
                print(f"Status Word: 0x{status:04X} ({status})")
                
                if status & 0x0001:
                    print("Ready to switch on")
                if status & 0x0002:
                    print("Switched on")
                if status & 0x0004:
                    print("Operation enabled")
                if status & 0x0008:
                    print("Fault detected")
                if status & 0x0010:
                    print("Voltage enabled")
                if status & 0x0020:
                    print("Quick stop")
                if status & 0x0040:
                    print("Switch on disabled")
                if status & 0x0080:
                    print("Warning")
                
                return status
            else:
                print("Failed to read status")
                return None
        except Exception as e:
            print(f"Error reading status: {e}")
            return None
    
    def read_frequency(self):
        try:
            result = self.client.read_holding_registers(self.ACTUAL_FREQ)
            if hasattr(result, 'registers') and result.registers:
                freq = result.registers[0] / 10.0
                print(f"Current Frequency: {freq} Hz")
                return freq
            else:
                print("Failed to read frequency")
                return None
        except Exception as e:
            print(f"Error reading frequency: {e}")
            return None
    
    def read_current(self):
        try:
            result = self.client.read_holding_registers(self.MOTOR_CURRENT)
            if hasattr(result, 'registers') and result.registers:
                current = result.registers[0] / 10.0  
                print(f"Motor Current: {current} A")
                return current
            else:
                print("Failed to read current")
                return None
        except Exception as e:
            print(f"Error reading current: {e}")
            return None
    
    def set_frequency(self, frequency_hz):
        try:
            freq_value = int(frequency_hz * 10)
            
            result = self.client.write_register(self.FREQ_REFERENCE, freq_value)
            if hasattr(result, 'isError') and not result.isError():
                print(f"Frequency set to {frequency_hz} Hz")
                return True
            else:
                print(f"Failed to set frequency: {result}")
                return False
        except Exception as e:
            print(f"Error setting frequency: {e}")
            return False
    
    def send_command(self, command, description=""):
        try:
            result = self.client.write_register(self.COMMAND_WORD, command)
            if hasattr(result, 'isError') and not result.isError():
                print(f"Command sent: {description} (0x{command:04X})")
                return True
            else:
                print(f"Failed to send command: {result}")
                return False
        except Exception as e:
            print(f"Error sending command: {e}")
            return False
    
    def start_motor(self, frequency_hz=25.0, direction='forward'):
        print(f"\n=== Starting Motor ===")
        print(f"Target Frequency: {frequency_hz} Hz")
        print(f"Direction: {direction}")
        
        if not self.set_frequency(frequency_hz):
            return False
        
        time.sleep(0.5)
        
        print("Step 1: Enabling drive...")
        if not self.send_command(self.CMD_STOP, "Enable Drive"):
            return False
        
        time.sleep(0.5)
        
        print("Step 2: Starting motor...")
        if direction.lower() == 'forward':
            command = 0x047F
            desc = "Run Forward via Ethernet"
        else:
            command = 0x043F
            desc = "Run Reverse via Ethernet"
        
        if not self.send_command(command, desc):
            return False
        
        print("Step 3: Verifying startup...")
        time.sleep(2.0)
        
        status = self.read_status()
        freq = self.read_frequency()
        
        if status and (status & 0x0004):  
            print("Motor started successfully via Ethernet!")
            self.read_current()
            return True
        else:
            print("Motor failed to start")
            return False
    
    def stop_motor(self):
        print(f"\n=== Stopping Motor ===")
        
        if self.send_command(self.CMD_STOP, "Controlled Stop"):
            time.sleep(1.0)
            status = self.read_status()
            if status:
                print("Motor stopped")
                return True
        
        print("Failed to stop motor")
        return False
    
    def emergency_stop(self):
        print(f"\n=== Emergency Stop ===")
        return self.send_command(self.CMD_EMERGENCY_STOP, "Emergency Stop")
    
    def reset_fault(self):
        print(f"\n=== Resetting Faults ===")
        return self.send_command(self.CMD_RESET_FAULT, "Reset Fault")
    
    def monitor_drive(self, duration=10):
        print(f"\n=== Monitoring Drive for {duration} seconds ===")
        
        for i in range(duration):
            print(f"\n--- Second {i+1} ---")
            self.read_status()
            self.read_frequency()
            self.read_current()
            time.sleep(1)

def main():
    print("ATV630U22N4 Motor Control Program")
    print("=" * 40)
    
    controller = ATV630Controller()
    
    if not controller.connect():
        sys.exit(1)
    
    try:
        while True:
            print("\n" + "=" * 40)
            print("ATV630 Motor Control Menu:")
            print("1. Read Status")
            print("2. Start Motor (Forward)")
            print("3. Start Motor (Reverse)")
            print("4. Stop Motor")
            print("5. Emergency Stop")
            print("6. Reset Faults")
            print("7. Set Frequency")
            print("8. Monitor Drive")
            print("9. Exit")
            print("=" * 40)
            
            choice = input("Enter choice (1-9): ").strip()
            
            if choice == '1':
                controller.read_status()
                controller.read_frequency()
                controller.read_current()
            
            elif choice == '2':
                freq = float(input("Enter frequency (Hz, default 25): ") or "25")
                controller.start_motor(freq, 'forward')
            
            elif choice == '3':
                freq = float(input("Enter frequency (Hz, default 25): ") or "25")
                controller.start_motor(freq, 'reverse')
            
            elif choice == '4':
                controller.stop_motor()
            
            elif choice == '5':
                controller.emergency_stop()
            
            elif choice == '6':
                controller.reset_fault()
            
            elif choice == '7':
                freq = float(input("Enter new frequency (Hz): "))
                controller.set_frequency(freq)
            
            elif choice == '8':
                duration = int(input("Monitor duration (seconds, default 10): ") or "10")
                controller.monitor_drive(duration)
            
            elif choice == '9':
                print("Exiting...")
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
    
    except Exception as e:
        print(f"\nUnexpected error: {e}")
    
    finally:
        controller.disconnect()

if __name__ == "__main__":
    main()
