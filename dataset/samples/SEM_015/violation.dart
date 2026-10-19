import 'package:flutter/material.dart';

class ColorSwatchPicker extends StatelessWidget {
  final Map<String, Color> colors;
  final String selectedColor;
  final ValueChanged<String> onSelected;

  const ColorSwatchPicker({
    super.key,
    required this.colors,
    required this.selectedColor,
    required this.onSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Wrap(
      children: [
        for (final entry in colors.entries)
          GestureDetector(
            behavior: HitTestBehavior.opaque,
            onTap: () => onSelected(entry.key),
            child: SizedBox(
              width: 48,
              height: 48,
              child: Center(
                child: Container(
                  width: 32,
                  height: 32,
                  decoration: BoxDecoration(
                    color: entry.value,
                    shape: BoxShape.circle,
                    border: Border.all(
                      color: entry.key == selectedColor
                          ? Colors.black
                          : Colors.transparent,
                      width: 3,
                    ),
                  ),
                ),
              ),
            ),
          ),
      ],
    );
  }
}
