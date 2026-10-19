import 'package:flutter/material.dart';

const Color shrineBrown900 = Color(0xFF442B2D);
const Color shrinePink400 = Color(0xFFEAA4A4);

class CategoryMenuItem extends StatelessWidget {
  const CategoryMenuItem({
    super.key,
    required this.categoryName,
    required this.isSelected,
    required this.onCategoryTap,
  });

  final String categoryName;
  final bool isSelected;
  final VoidCallback onCategoryTap;

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
    final selectedCategoryTextStyle =
        Theme.of(context).textTheme.bodyLarge!.copyWith(fontSize: 19);

    final unselectedCategoryTextStyle = selectedCategoryTextStyle.copyWith(
        color: shrineBrown900.withValues(alpha: 0.6));

    const indicatorHeight = 30.0;
    const indicatorWidth = indicatorHeight * 34 / 28;

    return Semantics(
      button: true,
      enabled: true,
      child: MouseRegion(
        cursor: SystemMouseCursors.click,
        child: GestureDetector(
          onTap: onCategoryTap,
          child: isSelected
              ? CustomPaint(
                  painter: const TriangleCategoryIndicator(
                    indicatorWidth,
                    indicatorHeight,
                  ),
                  child: _buttonText(categoryName, selectedCategoryTextStyle),
                )
              : _buttonText(categoryName, unselectedCategoryTextStyle),
        ),
      ),
    );
  }
}

const List<Offset> _vertices = [
  Offset(0, -14),
  Offset(-17, 14),
  Offset(17, 14),
  Offset(0, -14),
  Offset(0, -7.37),
  Offset(10.855, 10.48),
  Offset(-10.855, 10.48),
  Offset(0, -7.37),
];

class TriangleCategoryIndicator extends CustomPainter {
  const TriangleCategoryIndicator(
    this.triangleWidth,
    this.triangleHeight,
  );

  final double triangleWidth;
  final double triangleHeight;

  @override
  void paint(Canvas canvas, Size size) {
    final myPath = Path()
      ..addPolygon(
        List.from(_vertices.map<Offset>((vertex) {
          return Offset(size.width, size.height) / 2 +
              Offset(vertex.dx * triangleWidth / 34,
                  vertex.dy * triangleHeight / 28);
        })),
        true,
      );
    final myPaint = Paint()..color = shrinePink400;
    canvas.drawPath(myPath, myPaint);
  }

  @override
  bool shouldRepaint(TriangleCategoryIndicator oldDelegate) => false;

  @override
  bool shouldRebuildSemantics(TriangleCategoryIndicator oldDelegate) => false;
}
