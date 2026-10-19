import 'package:flutter/material.dart';

class SlideshowButtons extends StatefulWidget {
  const SlideshowButtons({
    required this.totalPages,
    required this.controller,
    required this.navigationLabel,
    super.key,
  });

  final int totalPages;
  final PageController controller;
  final String navigationLabel;

  @override
  State<SlideshowButtons> createState() => _SlideshowButtonsState();
}

class _SlideshowButtonsState extends State<SlideshowButtons> {
  int _currentPage = 0;
  static const _pageAnimationDuration = Duration(milliseconds: 300);

  @override
  void initState() {
    widget.controller.addListener(_onPageChanged);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final navigationBarLabel =
        '${_currentPage + 1} ${widget.navigationLabel} ${widget.totalPages}';

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          IconButton(
            key: const Key('slideshow_slideshowButtonsLeft'),
            onPressed: () async {
              if (_currentPage >= 1) {
                await widget.controller.previousPage(
                  duration: _pageAnimationDuration,
                  curve: Curves.easeInOut,
                );
              }
            },
            icon: _currentPage == 0
                ? const Icon(Icons.arrow_back, color: Colors.white38)
                : const Icon(Icons.arrow_back, color: Colors.white),
          ),
          Text(
            navigationBarLabel,
            style: theme.textTheme.titleLarge?.apply(color: Colors.white),
          ),
          IconButton(
            key: const Key('slideshow_slideshowButtonsRight'),
            onPressed: () async {
              if (_currentPage < widget.totalPages - 1) {
                await widget.controller.nextPage(
                  duration: _pageAnimationDuration,
                  curve: Curves.easeInOut,
                );
              }
            },
            icon: _currentPage == widget.totalPages - 1
                ? const Icon(Icons.arrow_forward, color: Colors.white38)
                : const Icon(Icons.arrow_forward, color: Colors.white),
          ),
        ],
      ),
    );
  }

  void _onPageChanged() {
    setState(() {
      _currentPage = widget.controller.page?.toInt() ?? 0;
    });
  }
}
