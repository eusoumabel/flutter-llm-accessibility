import 'package:flutter/material.dart';

class WebViewBottomBar extends StatelessWidget {
  const WebViewBottomBar({
    required this.onBack,
    required this.onForward,
    required this.onReload,
    super.key,
  });

  final VoidCallback onBack;
  final VoidCallback onForward;
  final VoidCallback onReload;

  @override
  Widget build(BuildContext context) {
    final Color? backgroundColor = AppBarTheme.of(context).backgroundColor;

    return TooltipTheme(
      data: TooltipTheme.of(context).copyWith(preferBelow: false),
      child: Padding(
        padding: const EdgeInsetsDirectional.only(
          top: 4.0,
          start: 8.0 * 3,
        ),
        child: Row(
          children: <Widget>[
            Material(
              color: backgroundColor,
              borderRadius: const BorderRadius.all(Radius.circular(20.0)),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  IconButton(
                    icon: const Icon(Icons.arrow_back, size: 18.0),
                    tooltip: 'Previous',
                    enableFeedback: true,
                    onPressed: onBack,
                  ),
                  IconButton(
                    icon: const Icon(Icons.arrow_forward, size: 18.0),
                    tooltip: 'Next',
                    enableFeedback: true,
                    onPressed: onForward,
                  ),
                  IconButton(
                    icon: const Icon(Icons.refresh),
                    tooltip: 'Reload',
                    enableFeedback: true,
                    onPressed: onReload,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
