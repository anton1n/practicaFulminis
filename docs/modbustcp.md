# Modbus TCP expanation

<br>
## Construction of a modbus tcp data packet
| Transaction Identifier| Protocol Identifier | Length  | Unit Id | Function Code | Register | Data    |
| --------------------- | ------------------- | ------- | ------- | ------------- | -------- | ------- |
| 2 bytes               | 2 bytes             | 2 bytes | 1 byte  | 1 byte        | 2 bytes  | 2 bytes | 
