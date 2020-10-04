class GoalCalc:
    def __init__(self, goal):
        self.goal = goal
        pass

    def calc(self):
        remaining_distance_cm = (self.goal.target_dist_km.value * 100000) - self.goal.spent_distance_cm
        target_average_cm_ms = self.goal.target_average_km_h.value / 36
        remaining_time_ms = ((self.goal.spent_distance_cm + remaining_distance_cm) / target_average_cm_ms) - self.goal.spent_time_ms
        calc_required_average_cm_ms = remaining_distance_cm / remaining_time_ms
        self.goal.calc_required_average_km_h = calc_required_average_cm_ms *36


        self.goal.remaining_distance_km = remaining_distance_cm / 100000
        self.goal.remaining_time_min = remaining_time_ms / 60000

        # target_average = (spent_distance_cm + remaining_distance_km) / (spent_time_ms + remaining_time_ms)
        # (spent_time_ms + remaining_time_ms) = (spent_distance_cm + remaining_distance_km) / target_average
        # remaining_time_ms = ((spent_distance_cm + remaining_distance_km) / target_average) - spent_time_ms
        pass