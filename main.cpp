
#include <iostream>
#include <vector>
#include <memory>
#include <list>

enum class OrderType
{
  GoodTillCancel,
  FillandKill,
};

enum class Side
{
  Buy,
  Sell
};

/*
 * aliases for types
 * 32 bit integer; unsigned for nonnegative numbers
*/
using Price = std::int32_t;
using Quantity = std::uint32_t;
using OrderId = std::uint64_t;

/*
 * price and quantity struct for each price level
*/
struct LevelInfo
{
  Price price_;
  Quantity quantity_;
};

/*
 * vector to represent rows of bids/ask prices
*/
using LevelInfos = std::vector<LevelInfo>;

class OrderbookLevelInfos // API
{
public:
  OrderbookLevelInfos(const LevelInfos& bids, const LevelInfos& asks) 
    : bids_{bids}
    , asks_{asks} {}

  // mark as const since method should not change class data members
  const LevelInfos& GetBids() const { return bids_; }
  const LevelInfos& GetAsks() const { return asks_; }

private:
  LevelInfos bids_;
  LevelInfos asks_;
};

class Order // order object 
{
public:
  Order(OrderType orderType, OrderId orderId, Side side, Price price, Quantity quantity) 
    : orderType_(orderType)
    , orderId_(orderId)
    , side_(side)
    , price_(price)
    , remainingQuantity_(quantity)
    , initialQuantity_(quantity) {}
  
  OrderId GetOrderId() const { return orderId_; }
  Side GetSide() const { return side_; }
  Price GetPrice() const { return price_; }
  OrderType GetOrderType() const { return orderType_; }
  Quantity GetInitialQuantity() const { return initialQuantity_; }
  Quantity GetRemaningQuantity() const { return remainingQuantity_; }
  Quantity GetFilledQuantity() const { return initialQuantity_ - remainingQuantity_; }
  
  // API to fill order; decrement some quantity
  void Fill(Quantity quantity)
  {
    if (quantity > remainingQuantity_) {
      throw std::logic_error("order cannot be filled; not enough quantity.");
    }
    remainingQuantity_ -= quantity;
  }

private:
  OrderType orderType_;
  OrderId orderId_;
  Side side_;
  Price price_;
  Quantity remainingQuantity_;
  Quantity initialQuantity_;
};


/*
 * shared/smart pointer that manages object life cycle and cleanup 
 * shared_ptr keeps track of ownership and references
*/
using OrderPointer = std::shared_ptr<Order>;
using OrderPointers = std::list<OrderPointer>; // list ADT dispersed in memory


/*
 *
*/
class OrderModify
{
public:
  OrderModify(OrderId orderId, Side side, Price price, Quantity quantity)
    : orderId_(orderId) 
    , side_(side)
    , price_(price)
    , quantity_(quantity) {}
  
  OrderId GetOrderId() const { return orderId_; }
  Price GetPrice() const { return price_; }
  Side GetSide() const { return side_; }
  Quantity GetQuantity() const { return quantity_; }

  // transform existing order into modified
  // created a shared pointer
  OrderPointer ToOrderPointer(OrderType type) const
  {
    return std::make_shared<Order>(type, orderId_, side_, price_, quantity_);
  }
private:
  OrderId orderId_;
  Side side_;
  Price price_;
  Quantity quantity_;
};

int main() {
  std::cout << "hello world" << std::endl;

}