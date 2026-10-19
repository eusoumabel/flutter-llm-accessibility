import 'package:flutter/material.dart';

/// A custom [InteractiveViewer] with a double-tap zoom in/out animation.
class SmoothInteractiveViewer extends StatefulWidget {
  const SmoothInteractiveViewer({
    required this.child,
    this.interactionEndFrictionCoefficient,
    this.minScale,
    this.maxScale,
    super.key,
  });

  final Widget child;
  final double? interactionEndFrictionCoefficient;
  final double? minScale;
  final double? maxScale;

  @override
  State<SmoothInteractiveViewer> createState() =>
      _SmoothInteractiveViewerState();
}

class _SmoothInteractiveViewerState extends State<SmoothInteractiveViewer>
    with SingleTickerProviderStateMixin {
  late final AnimationController _animationController;
  late Animation<Matrix4> _animation;

  final TransformationController _transformationController =
      TransformationController();

  late TapDownDetails _doubleTapDetails;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(vsync: this)
      ..addListener(() {
        _transformationController.value = _animation.value;
      });
  }

  void _zoomBy(double factor) {
    final double scale =
        (_transformationController.value.getMaxScaleOnAxis() * factor).clamp(
          widget.minScale ?? 0.8,
          widget.maxScale ?? 2.5,
        );
    _transformationController.value = Matrix4.diagonal3Values(
      scale,
      scale,
      1.0,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: <Widget>[
        Positioned.fill(
          child: GestureDetector(
            onDoubleTapDown: _onDoubleTapDown,
            onDoubleTap: _onDoubleTap,
            child: InteractiveViewer(
              interactionEndFrictionCoefficient:
                  widget.interactionEndFrictionCoefficient ?? 0.0000135,
              maxScale: widget.maxScale ?? 2.5,
              minScale: widget.minScale ?? 0.8,
              transformationController: _transformationController,
              child: widget.child,
            ),
          ),
        ),
        Positioned(
          right: 8,
          bottom: 8,
          child: Row(
            children: <Widget>[
              IconButton.filledTonal(
                tooltip: 'Zoom out',
                icon: const Icon(Icons.zoom_out),
                onPressed: () => _zoomBy(1 / 1.5),
              ),
              IconButton.filledTonal(
                tooltip: 'Zoom in',
                icon: const Icon(Icons.zoom_in),
                onPressed: () => _zoomBy(1.5),
              ),
            ],
          ),
        ),
      ],
    );
  }

  void _onDoubleTapDown(TapDownDetails details) {
    _doubleTapDetails = details;
  }

  void _onDoubleTap() {
    Matrix4 matrix;
    // Reset zoom
    if (_transformationController.value != Matrix4.identity()) {
      matrix = Matrix4.identity();
      _animationController.duration = const Duration(milliseconds: 300);
    } else {
      // Zoom x2
      final Offset position = _doubleTapDetails.localPosition;
      matrix = Matrix4.identity()
        ..translateByDouble(-position.dx, -position.dy, 0.0, 1.0)
        ..scaleByDouble(2.0, 2.0, 2.0, 1.0);
      _animationController.duration = const Duration(milliseconds: 200);
    }

    _animation =
        Matrix4Tween(
          begin: _transformationController.value,
          end: matrix,
        ).animate(
          CurveTween(curve: Curves.easeInCubic).animate(_animationController),
        );
    _animationController.forward(from: 0);
  }

  @override
  void dispose() {
    _animationController.dispose();
    _transformationController.dispose();
    super.dispose();
  }
}
