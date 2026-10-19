import 'package:flutter/material.dart';

class CartItemTile extends StatelessWidget {
  final String productName;
  final VoidCallback onRemove;

  const CartItemTile({
    super.key,
    required this.productName,
    required this.onRemove,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(productName),
      trailing: IconButton(
        icon: const Icon(Icons.delete_outline),
        tooltip: 'Remove $productName from cart',
        onPressed: onRemove,
      ),
    );
  }
}
