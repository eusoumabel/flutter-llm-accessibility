import 'package:flutter/material.dart';

class FloorPlanViewer extends StatefulWidget {
  final ImageProvider floorPlan;

  const FloorPlanViewer({super.key, required this.floorPlan});

  @override
  State<FloorPlanViewer> createState() => _FloorPlanViewerState();
}

class _FloorPlanViewerState extends State<FloorPlanViewer> {
  final _controller = TransformationController();

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
      ],
    );
  }
}
