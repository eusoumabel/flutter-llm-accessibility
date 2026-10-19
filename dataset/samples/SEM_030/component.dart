import 'package:flutter/material.dart';

class ScanPageButton extends StatelessWidget {
  const ScanPageButton(
      {super.key,
      required this.onTap,
      required this.icon,
      this.label,
      this.semanticsLabel,
      required this.buttonColor,
      required this.buttonIconColor});

  final VoidCallback onTap;
  final IconData icon;
  final String? label;

  /// Name for the icon-only variant, which has no visible [label].
  final String? semanticsLabel;
  final Color buttonColor;
  final Color buttonIconColor;

  @override
  Widget build(BuildContext context) {
    return Semantics(
        button: true,
        enabled: true,
        label: semanticsLabel ?? label,
        onTap: onTap,
        excludeSemantics: true,
        child: GestureDetector(
            onTap: onTap,
            behavior: HitTestBehavior.opaque,
            child: Container(
              decoration:
                  BoxDecoration(color: buttonColor, borderRadius: BorderRadius.circular(99999)),
              child: Padding(
                padding: EdgeInsets.only(
                    top: 10,
                    bottom: 10,
                    left: label == null ? 10 : 16,
                    right: label == null ? 10 : 20),
                child: Row(
                  spacing: 10,
                  children: [
                    Icon(icon, size: 28, color: buttonIconColor),
                    if (label != null)
                      Text(label!,
                          style: TextStyle(
                              fontSize: 16, fontWeight: FontWeight.w500, color: buttonIconColor))
                  ],
                ),
              ),
            )));
  }
}
