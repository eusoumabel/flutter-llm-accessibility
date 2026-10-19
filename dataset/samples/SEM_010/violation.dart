import 'package:flutter/material.dart';

class DarkModeToggle extends StatelessWidget {
  final bool isOn;
  final ValueChanged<bool> onChanged;

  const DarkModeToggle({super.key, required this.isOn, required this.onChanged});

  @override
  Widget build(BuildContext context) {
    return Semantics(
      button: true,
      label: 'Dark mode',
      child: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: () => onChanged(!isOn),
        child: SizedBox(
          width: 64,
          height: 48,
          child: Center(
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              width: 52,
              height: 32,
              padding: const EdgeInsets.all(4),
              alignment: isOn ? Alignment.centerRight : Alignment.centerLeft,
              decoration: BoxDecoration(
                color: isOn ? Colors.indigo : Colors.grey.shade400,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Container(
                width: 24,
                height: 24,
                decoration: const BoxDecoration(
                  color: Colors.white,
                  shape: BoxShape.circle,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
