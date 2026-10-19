import 'package:flutter/material.dart';

class LoginButton extends StatelessWidget {
  const LoginButton({required this.onLogin, super.key});

  final VoidCallback onLogin;

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.login),
      iconSize: 18,
      padding: EdgeInsets.zero,
      constraints: const BoxConstraints(),
      style: const ButtonStyle(
        tapTargetSize: MaterialTapTargetSize.shrinkWrap,
      ),
      onPressed: onLogin,
      tooltip: 'Login',
    );
  }
}
