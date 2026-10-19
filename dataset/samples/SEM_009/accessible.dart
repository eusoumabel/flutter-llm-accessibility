import 'package:flutter/material.dart';

class TermsLink extends StatelessWidget {
  final VoidCallback onOpenTerms;

  const TermsLink({super.key, required this.onOpenTerms});

  @override
  Widget build(BuildContext context) {
    return Semantics(
      link: true,
      child: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: onOpenTerms,
        child: Container(
          constraints: const BoxConstraints(minHeight: 48),
          alignment: Alignment.centerLeft,
          child: Text(
            'Read the Terms of Service',
            style: TextStyle(
              color: Theme.of(context).colorScheme.primary,
              decoration: TextDecoration.underline,
            ),
          ),
        ),
      ),
    );
  }
}
