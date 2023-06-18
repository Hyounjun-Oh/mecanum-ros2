// Copyright 2021 ROBOTIS CO., LTD.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef READ_WRITE_NODE_HPP_
#define READ_WRITE_NODE_HPP_

#include <cstdio>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "rcutils/cmdline_parser.h"
#include "dynamixel_sdk/dynamixel_sdk.h"
#include "dynamixel_sdk_custom_interfaces/msg/set_position.hpp"
#include "dynamixel_sdk_custom_interfaces/srv/get_position.hpp"
#include "std_msgs/msg/int16.hpp"


class ReadWriteNode : public rclcpp::Node
{
public:
  using SetPosition = dynamixel_sdk_custom_interfaces::msg::SetPosition;
  using GetPosition = dynamixel_sdk_custom_interfaces::srv::GetPosition;
  using manipulator_flag = std_msgs::msg::Int16;
  ReadWriteNode();
  virtual ~ReadWriteNode();
  mani_flag_ = this->create_publisher<std_msgs::msg::Int16>("manipulator_flag", QOS_RKL10V);
  timer_ = this->create_wall_timer(std::chrono::milliseconds(500),std::bind(&ReadWriteNode::manipulatorFlag, this));
  void manipulatorFlag()
  {
    flag = 0;
    auto message = std_msgs::msg::Int16();
    // for(int id_iter = 0;id_iter < 7;id_iter++)
    // {
    //   int moving_status = packetHandler->read1ByteTx(
    //     portHandler,
    //     id_iter,
    //     122
    //   );
    //   if (moving_status == 1)
    //   {
    //     flag = 1;
    //   }
    // }
    message.data = flag;
    RCLCPP_INFO(this->get_logger(), "Publishing: '%d'", message.data);
    
    ReadWriteNode::mani_flag_->publish(message);
  }

private:
  rclcpp::Subscription<SetPosition>::SharedPtr set_position_subscriber_;
  rclcpp::Service<GetPosition>::SharedPtr get_position_server_;
  rclcpp::Publisher<std_msgs::msg::Int16>::SharedPtr mani_flag_;

  int present_position;
  int flag;
};

#endif  // READ_WRITE_NODE_HPP_
