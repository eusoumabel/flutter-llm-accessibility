import 'package:flutter/material.dart';

class UnsplashHomePage extends StatelessWidget {
  const UnsplashHomePage({
    required this.title,
    required this.hasEntries,
    required this.searchContent,
    required this.onSearch,
    super.key,
  });

  final String title;
  final bool hasEntries;
  final Widget searchContent;
  final VoidCallback onSearch;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: hasEntries
          ? searchContent
          : const Center(
              child: Text('Search for Photos using the Fab button'),
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: onSearch,
        child: const Icon(Icons.search),
      ),
    );
  }
}
