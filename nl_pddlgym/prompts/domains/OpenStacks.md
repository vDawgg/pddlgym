## Domain description

A robot is tasked with making a set of products that need to be shipped to fulfill a set of orders. This needs to be accomplished with a limited amount of open stacks of products the robot can work with concurrently.

The actions available to the robot are:
- open-new-stack
    - Opens a new stack to process orders.
- start-order
    - Assign an order to an open stack to be processed.
- setup-machine
    - Sets up the machine to create a specific product
- make-products
    - Makes the specific product. To ensure that the machine is working at optimal capacity, all orders for the specific product the machine is currently configured for need to already be assigned to a stack so they can be processed.
- ship-order
    - Ships a specific order with the desired products, assuming that they have been manufactured. Once an order is shipped, the stack occupied by the order is freed and can be used again.
