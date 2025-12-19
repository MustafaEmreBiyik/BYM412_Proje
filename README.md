# 🤖 HomeCleaner Bot - ROS 2 Humble + Gazebo Harmonic

> **Senior ROS 2 Developer Handover Documentation**  
> Last Updated: December 19, 2025

---

## 🤖 Project Overview

**Project Name:** HomeCleaner Bot  
**ROS Distribution:** ROS 2 Humble  
**Simulator:** Gazebo Harmonic (via ros_gz)  
**Goal:** Autonomous cleaning robot capable of SLAM-based mapping, Nav2 autonomous navigation, and full coverage path planning in a simulated 2+1 apartment environment.

**Key Features:**
- ✅ Differential drive mobile robot with LiDAR and IMU
- ✅ Realistic 2+1 apartment world (Living Room, Hallway, 2 Bedrooms)
- ✅ SLAM Toolbox integration for online mapping
- ✅ Nav2 stack for autonomous navigation
- ✅ TF2 tree: `map` → `odom` → `base_footprint` → `base_link`

---

## 📂 Current File Structure

```
BYM412_Proje/
├── Dockerfile                    # Docker configuration (TODO)
├── PROJECT_STRUCTURE.md          # Project documentation
├── src/
│   └── home_cleaner_bot_description/
│       ├── package.xml           # ROS 2 package manifest
│       ├── CMakeLists.txt        # Build configuration
│       │
│       ├── urdf/
│       │   └── home_cleaner.urdf.xacro    # Robot description (URDF/Xacro)
│       │
│       ├── worlds/
│       │   ├── my_home.sdf       # 2+1 Apartment Gazebo world (10x10m)
│       │   └── LAYOUT_DIAGRAM.txt # Visual layout reference
│       │
│       ├── config/
│       │   ├── mapper_params_online_async.yaml  # SLAM Toolbox config
│       │   └── nav2_params.yaml  # Nav2 stack parameters
│       │
│       ├── launch/
│       │   ├── gazebo.launch.py  # Gazebo + Robot Spawner
│       │   ├── slam.launch.py    # SLAM + Gazebo + RViz2
│       │   └── navigation.launch.py # Nav2 + Gazebo (post-mapping)
│       │
│       └── maps/                 # (Empty - will store saved maps)
│
├── build/                        # Colcon build artifacts
├── install/                      # Colcon install artifacts
└── log/                          # Build logs
```

---

## ✅ What is DONE (Status Check)

| Component | Status | File/Directory | Notes |
|-----------|--------|----------------|-------|
| **Robot Model (URDF)** | ✅ **DONE** | `urdf/home_cleaner.urdf.xacro` | Differential drive with LiDAR + IMU |
| **2+1 Apartment World** | ✅ **DONE** | `worlds/my_home.sdf` | 10x10m apartment with 4 rooms + doorways |
| **SLAM Configuration** | ✅ **DONE** | `config/mapper_params_online_async.yaml` | Async SLAM Toolbox params |
| **Nav2 Configuration** | ✅ **DONE** | `config/nav2_params.yaml` | Full Nav2 stack parameters |
| **Gazebo Launch** | ✅ **DONE** | `launch/gazebo.launch.py` | Spawns world + robot |
| **SLAM Launch** | ✅ **DONE** | `launch/slam.launch.py` | Integrated SLAM + Gazebo + RViz2 |
| **Nav2 Launch** | ✅ **DONE** | `launch/navigation.launch.py` | Nav2 stack with localization |
| **Coverage Script** | ❌ **TODO** | *(Not created yet)* | Python node for room-by-room coverage |
| **Dockerfile** | ❌ **TODO** | `Dockerfile` | Containerization setup |

---

## 🚀 How to Run (Commands)

### Prerequisites
```bash
# Source ROS 2 Humble
source /opt/ros/humble/setup.bash

# Clone repository (if not done)
git clone https://github.com/MustafaEmreBiyik/BYM412_Proje.git
cd BYM412_Proje

# Build the workspace
colcon build --symlink-install
source install/setup.bash
```

---

### 🗺️ **Step 1: SLAM Mapping Phase**
Launch Gazebo + SLAM Toolbox + RViz2 to create the map:

```bash
source install/setup.bash
ros2 launch home_cleaner_bot_description slam.launch.py
```

**What happens:**
- Gazebo simulator starts with `my_home.sdf` world
- Robot spawns at origin
- SLAM Toolbox begins online mapping
- RViz2 opens with map visualization

**Manual Control (in a new terminal):**
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

**Save the map (when exploration is complete):**
```bash
ros2 run nav2_map_server map_saver_cli -f ~/map
# This saves: ~/map.pgm and ~/map.yaml
# Move them to: src/home_cleaner_bot_description/maps/
```

---

### 🧭 **Step 2: Autonomous Navigation Phase**
After saving the map, launch Nav2 for autonomous navigation:

```bash
source install/setup.bash
ros2 launch home_cleaner_bot_description navigation.launch.py
```

**What happens:**
- Gazebo starts with the same world
- Robot localizes using AMCL (Adaptive Monte Carlo Localization)
- Nav2 stack activates (planner, controller, recovery behaviors)
- RViz2 opens with Nav2 tools

**Send a navigation goal:**
- In RViz2: Use "2D Goal Pose" button to click a target location
- Or via command line:
```bash
ros2 topic pub --once /goal_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'map'},
  pose: {
    position: {x: 3.0, y: 3.0, z: 0.0},
    orientation: {w: 1.0}
  }
}"
```

---

### 🎮 **Optional: Manual Teleop Control**
Control the robot manually at any time:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

**Controls:**
- `i` = Forward
- `j` = Rotate Left
- `l` = Rotate Right
- `,` = Backward
- `k` = Stop

---

## 🚧 NEXT TASKS (For the Teammate)

### 🎯 **Task 1: Create Coverage Logic Script**
**Goal:** Implement a Python node that commands the robot to systematically visit all rooms using Nav2.

**Requirements:**
- Use `nav2_simple_commander` API
- Define waypoints for each room:
  - Living Room: `(x=-2.0, y=0.0)`
  - Hallway: `(x=2.5, y=0.0)`
  - Bedroom 1: `(x=3.0, y=3.25)`
  - Bedroom 2: `(x=3.0, y=-3.25)`
- Implement a state machine: `IDLE → CLEANING → PAUSED → COMPLETED`
- Add ROS 2 services:
  - `/start_cleaning` (std_srvs/Trigger)
  - `/stop_cleaning` (std_srvs/Trigger)

**File to create:**
```
src/home_cleaner_bot_description/scripts/coverage_planner.py
```

**Reference:**
```python
from nav2_simple_commander.robot_navigator import BasicNavigator
# See: https://github.com/ros-planning/navigation2/tree/humble/nav2_simple_commander
```

---

### 🎯 **Task 2: Create Start/Stop Command Logic**
**Goal:** Expose ROS 2 services for external control.

**Requirements:**
- Service definitions:
  ```bash
  ros2 service call /start_cleaning std_srvs/srv/Trigger
  ros2 service call /stop_cleaning std_srvs/srv/Trigger
  ```
- Publish status updates to `/cleaning_status` topic

---

### 🎯 **Task 3: Create Dockerfile**
**Goal:** Containerize the entire project for easy deployment.

**Requirements:**
- Base image: `osrf/ros:humble-desktop`
- Install Gazebo Harmonic
- Copy workspace and build
- Entry point: Launch SLAM or Navigation
- Volume mount for maps

**File to create:**
```
Dockerfile
docker-compose.yml (optional)
```

---

## 🔧 Troubleshooting

### Issue: "No robot model in RViz2"
**Solution:** Ensure `robot_state_publisher` is running:
```bash
ros2 node list | grep robot_state_publisher
```

### Issue: "SLAM map not building"
**Solution:** Check LiDAR topic:
```bash
ros2 topic echo /scan
```

### Issue: "Nav2 cannot plan path"
**Solution:** 
1. Verify map is loaded: `ros2 topic echo /map`
2. Check costmaps: `ros2 topic list | grep costmap`
3. Set initial pose in RViz2 using "2D Pose Estimate"

---

## 📚 Dependencies

All dependencies are declared in [package.xml](src/home_cleaner_bot_description/package.xml):
- `rclcpp` (C++ ROS 2 client library)
- `ros_gz_sim`, `ros_gz_bridge` (Gazebo integration)
- `slam_toolbox` (SLAM)
- `nav2_bringup` (Navigation stack)
- `robot_state_publisher` (TF tree)
- `rviz2` (Visualization)

---

## 🧠 Prompt for AI Assistant

> **Copy-paste this to your AI helper:**

```
We are building a HomeCleaner Bot using ROS 2 Humble and Gazebo Harmonic.

✅ COMPLETED INFRASTRUCTURE:
- Robot URDF with differential drive, LiDAR, and IMU is located at `urdf/home_cleaner.urdf.xacro`
- 2+1 apartment Gazebo world (10x10m with 4 rooms) is at `worlds/my_home.sdf`
- SLAM Toolbox configuration is complete at `config/mapper_params_online_async.yaml`
- Nav2 stack parameters are configured at `config/nav2_params.yaml`
- Launch files are ready:
  - `launch/gazebo.launch.py` - Spawns Gazebo world + robot
  - `launch/slam.launch.py` - SLAM + mapping + RViz2
  - `launch/navigation.launch.py` - Nav2 autonomous navigation

✅ TF TREE:
map → odom → base_footprint → base_link → [sensors]

✅ ROOM COORDINATES (for waypoint navigation):
- Living Room: (x=-2.0, y=0.0)
- Hallway: (x=2.5, y=0.0)
- Bedroom 1: (x=3.0, y=3.25)
- Bedroom 2: (x=3.0, y=-3.25)

🎯 YOUR TASK:
Implement the Python Coverage Script using `nav2_simple_commander.BasicNavigator`.

The script should:
1. Subscribe to `/amcl_pose` to track robot position
2. Use `BasicNavigator.goToPose()` to send waypoints sequentially
3. Implement state machine: IDLE → CLEANING → PAUSED → COMPLETED
4. Expose ROS 2 services:
   - `/start_cleaning` (std_srvs/Trigger)
   - `/stop_cleaning` (std_srvs/Trigger)
5. Publish status to `/cleaning_status` (std_msgs/String)

File location: `src/home_cleaner_bot_description/scripts/coverage_planner.py`

Reference: https://github.com/ros-planning/navigation2/tree/humble/nav2_simple_commander

Package name: home_cleaner_bot_description
```

---

## 📞 Contact & Collaboration

**Maintainer:** @MustafaEmreBiyik  
**GitHub Repository:** https://github.com/MustafaEmreBiyik/BYM412_Proje

For questions, open an issue on GitHub or contact the development team.

---

**🎉 The foundation is solid. Time to make the robot clean autonomously! 🧹**
