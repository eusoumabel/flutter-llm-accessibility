import 'package:flutter/material.dart';

class OrderCard extends StatelessWidget {
  final String orderNumber;
  final String status;
  final VoidCallback onOpen;

  const OrderCard({
    super.key,
    required this.orderNumber,
    required this.status,
    required this.onOpen,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      button: true,
      label: 'Order $orderNumber, $status',
      excludeSemantics: true,
      onTap: onOpen,
      child: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: onOpen,
        child: Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Order #$orderNumber',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 4),
                Text(status),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
