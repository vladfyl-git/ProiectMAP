import argparse
import random
import time
import sys
import copy

class Car:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.departure_time = None

    @property
    def wait_time(self):
        if self.departure_time is not None:
            return self.departure_time - self.arrival_time
        return 0

class TrafficSimulator:
    def __init__(self, cars_total=100, cycle_time=30, green_time=20, lanes=1, arrival_rate=0.3):
        self.cars_total = cars_total
        self.cycle_time = cycle_time
        self.green_time = green_time
        self.lanes_count = lanes
        self.arrival_rate = arrival_rate
        
        self.lanes = [[] for _ in range(lanes)]
        self.processed_cars = []
        self.current_time = 0
        self.cars_generated = 0
        
        # Statistici
        self.max_congestion = 0
        self.total_congestion = 0

    def get_light_state(self, t):
        phase = t % self.cycle_time
        if phase < self.green_time - 3:
            return "VERDE", "\033[92m" # Green
        elif phase < self.green_time:
            return "GALBEN", "\033[93m" # Yellow
        else:
            return "ROSU", "\033[91m" # Red

    def run(self, visualize=False, duration=None):
        while self.cars_generated < self.cars_total or any(len(l) > 0 for l in self.lanes):
            if duration and self.current_time >= duration:
                break

            # 1. Generare mașini (Poisson-like)
            if self.cars_generated < self.cars_total:
                if random.random() < self.arrival_rate:
                    # Adăugăm mașina pe banda cea mai liberă
                    shortest_lane = min(self.lanes, key=len)
                    shortest_lane.append(Car(self.current_time))
                    self.cars_generated += 1

            # 2. Procesare trafic (Semafor)
            state, color_code = self.get_light_state(self.current_time)
            if state in ["VERDE", "GALBEN"]:
                for lane in self.lanes:
                    if lane:
                        car = lane.pop(0)
                        car.departure_time = self.current_time
                        self.processed_cars.append(car)

            # 3. Colectare date
            current_queue = sum(len(l) for l in self.lanes)
            self.max_congestion = max(self.max_congestion, current_queue)
            self.total_congestion += current_queue

            # 4. Vizualizare
            if visualize:
                self._draw_frame(state, color_code, current_queue)
                time.sleep(0.05) # Viteza animației

            self.current_time += 1

        return self.get_report()

    def _draw_frame(self, state, color, queue_size):
        sys.stdout.write("\033[H\033[J") # Clear screen
        print(f"       Simulator Trafic Rutier")
        print(f" t={self.current_time}s")
        print(f" [{color}{state:^10}\033[0m]")
        
        for i, lane in enumerate(self.lanes):
            visual_queue = "█" * len(lane) + "░" * (10 - len(lane))
            print(f" Banda {i+1}: {visual_queue} ({len(lane)} mașini)")
        
        print("-" * 30)
        print(f" Mașini procesate: {len(self.processed_cars)}/{self.cars_total}")
        print(f" Congestie medie: {self.total_congestion / (self.current_time if self.current_time > 0 else 1):.1f}")
        sys.stdout.flush()

    def get_report(self):
        wait_times = [c.wait_time for c in self.processed_cars]
        avg_wait = sum(wait_times) / len(wait_times) if wait_times else 0
        efficiency = (self.green_time / self.cycle_time) * 100
        
        return {
            "total_time": self.current_time,
            "avg_wait": avg_wait,
            "max_congestion": self.max_congestion,
            "avg_congestion": self.total_congestion / self.current_time if self.current_time > 0 else 0,
            "efficiency": efficiency,
            "processed": len(self.processed_cars)
        }

def optimize_params(args):
    print("Se caută configurarea optimă...")
    best_green = 20
    min_wait = float('inf')
    
    for g_time in range(10, args.light_cycle, 5):
        sim = TrafficSimulator(args.cars, args.light_cycle, g_time, args.lanes, args.arrival_rate)
        res = sim.run(visualize=False)
        if res['avg_wait'] < min_wait:
            min_wait = res['avg_wait']
            best_green = g_time
            
    print(f"→ Optimizare completă: Timp verde recomandat: {best_green}s")
    return best_green

def main():
    parser = argparse.ArgumentParser(description="Simulator Trafic Rutier")
    parser.add_argument("--cars", type=int, default=100)
    parser.add_argument("--light_cycle", type=int, default=30)
    parser.add_argument("--green_time", type=int, default=20)
    parser.add_argument("--lanes", type=int, default=1)
    parser.add_argument("--arrival_rate", type=float, default=0.3)
    parser.add_argument("--viz", action="store_true")
    parser.add_argument("--optimize", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--compare", type=str, help="Ex: '1,2,3' pentru comparare benzi")
    
    args = parser.parse_args()

    if args.compare:
        lane_options = [int(x) for x in args.compare.split(',')]
        print(f"Comparație număr benzi ({args.cars} mașini):")
        for l in lane_options:
            sim = TrafficSimulator(args.cars, args.light_cycle, args.green_time, l, args.arrival_rate)
            r = sim.run(visualize=False)
            print(f"  {l} benzi: Timp mediu așteptare: {r['avg_wait']:.1f}s, Congestie max: {r['max_congestion']}")
        return

    g_time = args.green_time
    if args.optimize:
        g_time = optimize_params(args)

    sim = TrafficSimulator(args.cars, args.light_cycle, g_time, args.lanes, args.arrival_rate)
    report = sim.run(visualize=args.viz)

    print("\n" + "="*20 + " RAPORT FINAL " + "="*20)
    print(f"Total mașini: {args.cars}")
    print(f"Timp total simulare: {report['total_time']} secunde")
    print(f"Congestie medie: {report['avg_congestion']:.2f} mașini")
    print(f"Congestie maximă: {report['max_congestion']} mașini")
    print(f"Timp așteptare mediu: {report['avg_wait']:.2f} secunde")
    print(f"Eficiență semafor: {report['efficiency']:.0f}%")

if __name__ == "__main__":
    main()