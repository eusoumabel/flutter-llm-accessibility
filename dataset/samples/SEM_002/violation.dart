import 'package:flutter/material.dart';

class ArticleHeader extends StatelessWidget {
  final String title;
  final VoidCallback onShare;

  const ArticleHeader({super.key, required this.title, required this.onShare});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Semantics(
            header: true,
            child: Text(title, style: Theme.of(context).textTheme.titleLarge),
          ),
        ),
        IconButton(
          icon: const Icon(Icons.share),
          onPressed: onShare,
        ),
      ],
    );
  }
}
