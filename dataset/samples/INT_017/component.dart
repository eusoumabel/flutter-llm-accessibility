import 'package:flutter/material.dart';

class SmoothCardHeaderButton extends StatelessWidget {
  const SmoothCardHeaderButton({
    required this.tooltip,
    required this.child,
    required this.onTap,
    this.circled = false,
    this.padding,
    super.key,
  });

  final String tooltip;
  final Widget child;
  final VoidCallback onTap;
  final bool circled;
  final EdgeInsetsGeometry? padding;

  @override
  Widget build(BuildContext context) {
    Widget child = Padding(
      padding: padding ?? const EdgeInsetsDirectional.all(12.0),
      child: this.child,
    );

    if (circled) {
      child = Material(
        color: Colors.transparent,
        shape: const CircleBorder(
          side: BorderSide(width: 1.0, color: Colors.white),
        ),
        child: child,
      );
    }

    return Material(
      type: MaterialType.transparency,
      child: Semantics(
        label: tooltip,
        button: true,
        excludeSemantics: true,
        child: Tooltip(
          message: tooltip,
          child: InkWell(
            customBorder: const CircleBorder(),
            onTap: onTap,
            child: child,
          ),
        ),
      ),
    );
  }
}
