// L7: load place_cell.xml with BehaviorTree.CPP 4 and tick it.
// Usage: place_cell XML FAILURES. The mock PickFromTester fails
// FAILURES times, then succeeds. Node names are examples.
#include <behaviortree_cpp/bt_factory.h>

#include <filesystem>
#include <iostream>
#include <string>

using namespace BT;

int failures_left{0};

class PickFromTester : public SyncActionNode {
 public:
  PickFromTester(const std::string& name, const NodeConfig& config)
      : SyncActionNode(name, config) {}
  static PortsList providedPorts() {
    return {InputPort<std::string>("tester")};
  }
  NodeStatus tick() override {
    auto tester = getInput<std::string>("tester");
    bool ok{failures_left == 0};
    if (!ok) { failures_left -= 1; }
    std::cout << "pick from " << tester.value() << ": "
              << (ok ? "SUCCESS" : "FAILURE") << '\n';
    return ok ? NodeStatus::SUCCESS : NodeStatus::FAILURE;
  }
};

class PlaceInSlot : public SyncActionNode {
 public:
  PlaceInSlot(const std::string& name, const NodeConfig& config)
      : SyncActionNode(name, config) {}
  static PortsList providedPorts() {
    return {InputPort<std::string>("agv"), InputPort<int>("slot")};
  }
  NodeStatus tick() override {
    std::cout << "place on " << getInput<std::string>("agv").value()
              << " slot " << getInput<int>("slot").value() << '\n';
    return NodeStatus::SUCCESS;
  }
};

int main(int argc, char** argv) {
  failures_left = std::stoi(argv[2]);
  BehaviorTreeFactory factory;
  factory.registerNodeType<PickFromTester>("PickFromTester");
  factory.registerNodeType<PlaceInSlot>("PlaceInSlot");
  auto tree = factory.createTreeFromFile(  // needs a full path
      std::filesystem::absolute(argv[1]));
  auto blackboard = tree.rootBlackboard();
  blackboard->set("tester", std::string("tester1"));
  blackboard->set("agv", std::string("agv1"));
  blackboard->set("slot", 2);
  NodeStatus status{tree.tickWhileRunning()};
  std::cout << "tree: " << toStr(status) << '\n';
}
