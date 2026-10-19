import 'package:flutter/material.dart';

class TermsCheckbox extends StatelessWidget {
  final bool accepted;
  final ValueChanged<bool> onChanged;

  const TermsCheckbox({
    super.key,
    required this.accepted,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Semantics(
          checked: accepted,
          label: 'I accept the terms and conditions',
          child: GestureDetector(
            behavior: HitTestBehavior.opaque,
            onTap: () => onChanged(!accepted),
            child: SizedBox(
              width: 48,
              height: 48,
              child: Center(
                child: Container(
                  width: 24,
                  height: 24,
                  decoration: BoxDecoration(
                    color: accepted ? Colors.blue : Colors.transparent,
                    border: Border.all(color: Colors.blue, width: 2),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: accepted
                      ? const Icon(Icons.check, size: 18, color: Colors.white)
                      : null,
                ),
              ),
            ),
          ),
        ),
        const Expanded(
          child: ExcludeSemantics(
            child: Text('I accept the terms and conditions'),
          ),
        ),
      ],
    );
  }
}
