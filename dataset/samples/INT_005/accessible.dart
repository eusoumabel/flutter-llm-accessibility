import 'package:flutter/material.dart';

class FloorPlanViewer extends StatefulWidget {
  final ImageProvider floorPlan;

  const FloorPlanViewer({super.key, required this.floorPlan});

  @override
  State<FloorPlanViewer> createState() => _FloorPlanViewerState();
}

class _FloorPlanViewerState extends State<FloorPlanViewer> {
  final _controller = TransformationController();
  double _scale = 1.0;

  void _setScale(double value) {
    _scale = value.clamp(1.0, 4.0);
    _controller.value = Matrix4.diagonal3Values(_scale, _scale, 1.0);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Expanded(
          child: InteractiveViewer(
            transformationController: _controller,
            minScale: 1.0,
            maxScale: 4.0,
            child: Image(
              image: widget.floorPlan,
              semanticLabel: 'Office floor plan',
            ),
          ),
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            IconButton(
              icon: const Icon(Icons.zoom_out),
              tooltip: 'Zoom out',
              onPressed: () => _setScale(_scale - 0.5),
            ),
            IconButton(
              icon: const Icon(Icons.zoom_in),
              tooltip: 'Zoom in',
              onPressed: () => _setScale(_scale + 0.5),
            ),
          ],
        ),
      ],
    );
  }
}
