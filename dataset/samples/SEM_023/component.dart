import 'package:flutter/material.dart';

class DesktopProductCard extends StatelessWidget {
  const DesktopProductCard({
    super.key,
    required this.name,
    required this.price,
    required this.image,
    required this.imageWidth,
    required this.onAddToCart,
  });

  final String name;
  final int price;
  final ImageProvider image;
  final double imageWidth;
  final VoidCallback onAddToCart;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final imageWidget = Image(
      image: image,
      fit: BoxFit.cover,
      width: imageWidth,
      excludeFromSemantics: true,
    );

    return Semantics(
      hint: 'Add to cart',
      child: MouseRegion(
        cursor: SystemMouseCursors.click,
        child: GestureDetector(
          onTap: onAddToCart,
          child: Stack(
            children: [
              Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  imageWidget,
                  SizedBox(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        const SizedBox(height: 23),
                        SizedBox(
                          width: imageWidth,
                          child: Text(
                            name,
                            style: theme.textTheme.labelLarge,
                            softWrap: true,
                            textAlign: TextAlign.center,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          '\$$price',
                          style: theme.textTheme.bodySmall,
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const Padding(
                padding: EdgeInsets.all(16),
                child: Icon(Icons.add_shopping_cart),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
