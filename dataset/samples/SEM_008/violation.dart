import 'package:flutter/material.dart';

class RecentOrdersSection extends StatelessWidget {
  final List<String> orders;

  const RecentOrdersSection({super.key, required this.orders});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Recent orders',
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const SizedBox(height: 8),
        for (final order in orders) ListTile(title: Text(order)),
      ],
    );
  }
}
