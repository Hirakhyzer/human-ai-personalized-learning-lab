function plot_learning_curves(outputs_dir)
%PLOT_LEARNING_CURVES Plot synthetic mastery curves from Python output.
% Usage: plot_learning_curves('outputs')

if nargin < 1
    outputs_dir = fullfile('..', 'outputs');
end
input_path = fullfile(outputs_dir, 'results', 'synthetic_learning_activity.csv');
if ~isfile(input_path)
    error('Missing %s. Run scripts/run_synthetic_learning_lab.py first.', input_path);
end
T = readtable(input_path);
modes = unique(T.feedback_mode);
figure('Color', 'w', 'Position', [100 100 980 430]);
hold on;
for i = 1:numel(modes)
    mode = modes{i};
    idx = strcmp(T.feedback_mode, mode);
    sessions = unique(T.session(idx));
    curve = zeros(size(sessions));
    for j = 1:numel(sessions)
        curve(j) = mean(T.mastery_estimate(idx & T.session == sessions(j)));
    end
    plot(sessions, curve, '-o', 'DisplayName', mode, 'LineWidth', 1.2);
end
grid on;
xlabel('Session'); ylabel('Mean mastery estimate');
title('Synthetic Human-AI learning mastery curves');
legend('Location', 'best');
exportgraphics(gcf, fullfile(outputs_dir, 'figures', 'synthetic_mastery_curves_matlab.png'), 'Resolution', 250);
end
