import 'package:flutter/material.dart';

class LoginButton extends StatelessWidget {
  const LoginButton({required this.onLogin, super.key});

  final VoidCallback onLogin;

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.login),
      iconSize: 24,
      padding: const EdgeInsets.symmetric(
        horizontal: 16,
        vertical: 8,
      ),
      onPressed: onLogin,
      tooltip: 'Login',
    );
  }
}
