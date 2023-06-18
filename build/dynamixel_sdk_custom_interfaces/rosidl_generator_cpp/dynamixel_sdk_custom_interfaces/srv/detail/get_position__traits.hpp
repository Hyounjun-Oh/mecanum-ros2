// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from dynamixel_sdk_custom_interfaces:srv/GetPosition.idl
// generated code does not contain a copyright notice

#ifndef DYNAMIXEL_SDK_CUSTOM_INTERFACES__SRV__DETAIL__GET_POSITION__TRAITS_HPP_
#define DYNAMIXEL_SDK_CUSTOM_INTERFACES__SRV__DETAIL__GET_POSITION__TRAITS_HPP_

#include "dynamixel_sdk_custom_interfaces/srv/detail/get_position__struct.hpp"
#include <stdint.h>
#include <rosidl_runtime_cpp/traits.hpp>
#include <sstream>
#include <string>
#include <type_traits>

namespace rosidl_generator_traits
{

inline void to_yaml(
  const dynamixel_sdk_custom_interfaces::srv::GetPosition_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    value_to_yaml(msg.id, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const dynamixel_sdk_custom_interfaces::srv::GetPosition_Request & msg)
{
  std::ostringstream out;
  to_yaml(msg, out);
  return out.str();
}

template<>
inline const char * data_type<dynamixel_sdk_custom_interfaces::srv::GetPosition_Request>()
{
  return "dynamixel_sdk_custom_interfaces::srv::GetPosition_Request";
}

template<>
inline const char * name<dynamixel_sdk_custom_interfaces::srv::GetPosition_Request>()
{
  return "dynamixel_sdk_custom_interfaces/srv/GetPosition_Request";
}

template<>
struct has_fixed_size<dynamixel_sdk_custom_interfaces::srv::GetPosition_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dynamixel_sdk_custom_interfaces::srv::GetPosition_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dynamixel_sdk_custom_interfaces::srv::GetPosition_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

inline void to_yaml(
  const dynamixel_sdk_custom_interfaces::srv::GetPosition_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position: ";
    value_to_yaml(msg.position, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const dynamixel_sdk_custom_interfaces::srv::GetPosition_Response & msg)
{
  std::ostringstream out;
  to_yaml(msg, out);
  return out.str();
}

template<>
inline const char * data_type<dynamixel_sdk_custom_interfaces::srv::GetPosition_Response>()
{
  return "dynamixel_sdk_custom_interfaces::srv::GetPosition_Response";
}

template<>
inline const char * name<dynamixel_sdk_custom_interfaces::srv::GetPosition_Response>()
{
  return "dynamixel_sdk_custom_interfaces/srv/GetPosition_Response";
}

template<>
struct has_fixed_size<dynamixel_sdk_custom_interfaces::srv::GetPosition_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dynamixel_sdk_custom_interfaces::srv::GetPosition_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dynamixel_sdk_custom_interfaces::srv::GetPosition_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<dynamixel_sdk_custom_interfaces::srv::GetPosition>()
{
  return "dynamixel_sdk_custom_interfaces::srv::GetPosition";
}

template<>
inline const char * name<dynamixel_sdk_custom_interfaces::srv::GetPosition>()
{
  return "dynamixel_sdk_custom_interfaces/srv/GetPosition";
}

template<>
struct has_fixed_size<dynamixel_sdk_custom_interfaces::srv::GetPosition>
  : std::integral_constant<
    bool,
    has_fixed_size<dynamixel_sdk_custom_interfaces::srv::GetPosition_Request>::value &&
    has_fixed_size<dynamixel_sdk_custom_interfaces::srv::GetPosition_Response>::value
  >
{
};

template<>
struct has_bounded_size<dynamixel_sdk_custom_interfaces::srv::GetPosition>
  : std::integral_constant<
    bool,
    has_bounded_size<dynamixel_sdk_custom_interfaces::srv::GetPosition_Request>::value &&
    has_bounded_size<dynamixel_sdk_custom_interfaces::srv::GetPosition_Response>::value
  >
{
};

template<>
struct is_service<dynamixel_sdk_custom_interfaces::srv::GetPosition>
  : std::true_type
{
};

template<>
struct is_service_request<dynamixel_sdk_custom_interfaces::srv::GetPosition_Request>
  : std::true_type
{
};

template<>
struct is_service_response<dynamixel_sdk_custom_interfaces::srv::GetPosition_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // DYNAMIXEL_SDK_CUSTOM_INTERFACES__SRV__DETAIL__GET_POSITION__TRAITS_HPP_
