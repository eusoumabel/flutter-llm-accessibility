import 'package:flutter/material.dart';

class OrderStatusRow extends StatelessWidget {
  final String orderNumber;
  final bool delivered;

  const OrderStatusRow({
    super.key,
    required this.orderNumber,
    required this.delivered,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Text('Order #$orderNumber'),
        const SizedBox(width: 8),
        Icon(
          delivered ? Icons.check_circle : Icons.schedule,
          color: delivered ? Colors.green : Colors.orange,
          semanticLabel: '',
        ),
      ],
    );
  }
}
