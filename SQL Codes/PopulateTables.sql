-- Populate USER table
-- passwords are stored as hash please read the documentation for more details
INSERT INTO USER (UID, Name, Email, Password, PhoneNumber)
VALUES 
('1RV24PFMGMT0001', 'Alice', 'alice@example.com', 'password123', '+919876543201'),
('1RV24PFMGMT0002', 'Bob', 'bob@example.com', 'password456', '+918765432109'),
('1RV24PFMGMT0003', 'Charlie', 'charlie@example.com', 'password789', '+919012345678'),
('1RV24PFMGMT0004', 'David', 'david@example.com', 'password321', '+918765432112'),
('1RV24PFMGMT0005', 'Eve', 'eve@example.com', 'password654', '+919876543210'),
('1RV24PFMGMT0006', 'Frank', 'frank@example.com', 'password987', '+918765432113'),
('1RV24PFMGMT0007', 'Grace', 'grace@example.com', 'password654', '+919012345679');

-- Populate PORTFOLIO table
INSERT INTO PORTFOLIO (portID, portName, UID)
VALUES 
('RVCEPTFL0001', 'Mutual funds', '1RV24PFMGMT0001'),
('RVCEPTFL0002', 'Equity', '1RV24PFMGMT0002'),
('RVCEPTFL0003', 'Mutual funds', '1RV24PFMGMT0001'),
('RVCEPTFL0004', 'Mutual funds', '1RV24PFMGMT0002'),
('RVCEPTFL0005', 'Equity', '1RV24PFMGMT0001'),
('RVCEPTFL0006', 'Equity', '1RV24PFMGMT0002'),
('RVCEPTFL0007', 'Mutual funds', '1RV24PFMGMT0003');

-- Populate STOCK table
INSERT INTO STOCK (stockID, OPEN, CLOSE, HIGH, LOW, Curr)
VALUES 
('RVCESTOCK0001', 100.00, 105.50, 110.00, 95.00, 102.75),
('RVCESTOCK0002', 50.00, 52.75, 55.25, 48.50, 51.20),
('RVCESTOCK0003', 75.50, 80.25, 82.00, 73.50, 78.10),
('RVCESTOCK0004', 120.00, 115.75, 125.50, 112.00, 118.30),
('RVCESTOCK0005', 90.25, 92.50, 95.75, 88.00, 93.10),
('RVCESTOCK0006', 110.50, 112.75, 115.25, 108.50, 111.20),
('RVCESTOCK0007', 65.00, 67.25, 70.25, 62.50, 66.10);

-- Populate COMPANY table
INSERT INTO COMPANY (cCode, cName, cType)
VALUES 
('MSFT', 'Microsoft', 'Technology'),
('AAPL', 'Apple', 'Technology'),
('GOOGL', 'Alphabet Inc.', 'Technology'),
('AMZN', 'Amazon', 'Retail'),
('TSLA', 'Tesla', 'Automotive'),
('INTC', 'Intel', 'Technology'),
('NVDA', 'NVIDIA', 'Technology');

-- Populate MARKET table
INSERT INTO MARKET (mId, mIndex, tradingHours)
VALUES 
('RVCEMKT0001', 'NIFTY50', '09:00 - 15:30'),
('RVCEMKT0002', 'SENSEX', '09:00 - 15:30'),
('RVCEMKT0003', 'NASDAQ', '09:30 - 16:00'),
('RVCEMKT0004', 'DOWJONES', '09:30 - 16:00'),
('RVCEMKT0005', 'FTSE100', '08:00 - 16:30'),
('RVCEMKT0006', 'NIKKEI225', '09:00 - 15:00'),
('RVCEMKT0007', 'HANGSENG', '09:30 - 16:30');

-- Populate HAS table
INSERT INTO HAS (dateCreate, ownType, portId, stockId)
VALUES 
('2024-03-09', 'Individual', 'RVCEPTFL0001', 'RVCESTOCK0001'),
('2024-03-09', 'Individual', 'RVCEPTFL0002', 'RVCESTOCK0002'),
('2024-03-09', 'Individual', 'RVCEPTFL0003', 'RVCESTOCK0003'),
('2024-03-09', 'Individual', 'RVCEPTFL0004', 'RVCESTOCK0004'),
('2024-03-09', 'Individual', 'RVCEPTFL0005', 'RVCESTOCK0005'),
('2024-03-09', 'Individual', 'RVCEPTFL0006', 'RVCESTOCK0006'),
('2024-03-09', 'Individual', 'RVCEPTFL0007', 'RVCESTOCK0007');

-- Populate TRADEDBY table
INSERT INTO TRADEDBY (cName, cCode, stockId)
VALUES 
('Microsoft', 'MSFT', 'RVCESTOCK0001'),
('Apple Inc.', 'AAPL', 'RVCESTOCK0002'),
('Alphabet Inc.', 'GOOGL', 'RVCESTOCK0003'),
('Amazon.com Inc.', 'AMZN', 'RVCESTOCK0004'),
('Tesla Inc.', 'TSLA', 'RVCESTOCK0005'),
('Intel Corporation', 'INTC', 'RVCESTOCK0006'),
('NVIDIA Corporation', 'NVDA', 'RVCESTOCK0007');

-- Populate TRANSACTS table
INSERT INTO TRANSACTS (accNo, type, value, quantity, timestamp, portId, stockId)
VALUES 
('12345678901', 'Buy', 1500.00, 10, '2024-03-09 10:30:00', 'RVCEPTFL0001', 'RVCESTOCK0001'),
('23456789012', 'Sell', 800.00, 5, '2024-03-09 11:45:00', 'RVCEPTFL0002', 'RVCESTOCK0002'),
('34567890123', 'Buy', 2000.00, 8, '2024-03-09 13:15:00', 'RVCEPTFL0003', 'RVCESTOCK0003'),
('45678901234', 'Sell', 1200.00, 6, '2024-03-09 14:30:00', 'RVCEPTFL0004', 'RVCESTOCK0004'),
('56789012345', 'Buy', 2500.00, 12, '2024-03-09 15:45:00', 'RVCEPTFL0005', 'RVCESTOCK0005'),
('67890123456', 'Buy', 1800.00, 15, '2024-03-09 16:30:00', 'RVCEPTFL0006', 'RVCESTOCK0006'),
('78901234567', 'Sell', 1100.00, 8, '2024-03-09 17:15:00', 'RVCEPTFL0007', 'RVCESTOCK0007');

-- Populate LISTS table
INSERT INTO LISTS (timestamp, mId, cCode)
VALUES 
('2024-03-09 12:00:00', 'RVCEMKT0001', 'MSFT'),
('2024-03-09 12:00:00', 'RVCEMKT0002', 'AAPL'),
('2024-03-09 12:00:00', 'RVCEMKT0003', 'GOOGL'),
('2024-03-09 12:00:00', 'RVCEMKT0004', 'AMZN'),
('2024-03-09 12:00:00', 'RVCEMKT0005', 'TSLA'),
('2024-03-09 12:00:00', 'RVCEMKT0006', 'INTC'),
('2024-03-09 12:00:00', 'RVCEMKT0007', 'NVDA');