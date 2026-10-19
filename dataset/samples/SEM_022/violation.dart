import 'package:flutter/material.dart';

class DesktopCategoryHeader extends StatelessWidget {
  const DesktopCategoryHeader({
    super.key,
    required this.title,
    required this.asset,
  });

  final String title;
  final ImageProvider asset;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    return Material(
      color: colorScheme.onSurface,
      child: Row(
        children: [
          Padding(
            padding: const EdgeInsets.all(10),
            child: Image(
              image: asset,
              width: 64,
              height: 64,
              excludeFromSemantics: true,
            ),
          ),
          Flexible(
            child: Padding(
              padding: const EdgeInsetsDirectional.only(start: 8),
              child: SelectableText(
                title,
                style: Theme.of(context).textTheme.headlineSmall!.apply(
                      color: colorScheme.surface,
                    ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
