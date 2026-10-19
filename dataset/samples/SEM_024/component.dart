import 'package:flutter/material.dart';

class LogoutButton extends StatelessWidget {
  const LogoutButton({super.key, required this.onLogout});

  final VoidCallback onLogout;

  Widget _buttonText(String caption, TextStyle style) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: Text(
        caption,
        style: style,
        textAlign: TextAlign.center,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final logoutTextStyle = Theme.of(context).textTheme.bodyLarge!.copyWith(
          fontSize: 19,
          color: const Color(0xFF442B2D).withValues(alpha: 0.6),
        );

    return Semantics(
      button: true,
      enabled: true,
      child: MouseRegion(
        cursor: SystemMouseCursors.click,
        child: GestureDetector(
          onTap: onLogout,
          child: _buttonText('LOGOUT', logoutTextStyle),
        ),
      ),
    );
  }
}
