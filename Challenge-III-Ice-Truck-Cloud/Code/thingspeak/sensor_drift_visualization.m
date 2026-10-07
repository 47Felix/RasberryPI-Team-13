% Challenge III: Sensor-Drift (Predictive Maintenance)
% Zweck: Zeigt, ob die beiden Temperatursensoren (Sensor-Board und Aktor-Board) auseinanderlaufen.
%        Eine wachsende Abweichung deutet auf einen defekten Sensor oder einen Wackelkontakt
%        am KY-028 hin. So lässt sich die Wartung planen, bevor der Truck ausfällt.
% Einrichten: ThingSpeak -> Apps -> MATLAB Visualizations -> New -> "Custom (no starting code)",
%             dieses Skript einfügen, "Save and Run". Danach im Kanal über "Add Visualizations" anzeigen.
% Hinweis: Der Kanal ist öffentlich, ein Read Key ist nicht nötig. Bei privatem Kanal bei
%          thingSpeakRead zusätzlich 'ReadKey', '<READ_KEY>' ergänzen (Key nie ins Repository).

kanal      = 3516326;   % Channel ID
anzahl     = 8000;      % letzte Messungen (ThingSpeak liefert höchstens 8000 pro Abruf)
glaettung  = 40;        % Messungen pro gleitendem Mittelwert (ca. 3 min bei 5 s, 10 min bei 15 s)
schwelle   = 3;         % Grad Celsius, entspricht SENSOR_MISMATCH_C in der Bridge

% Field 1 = Temperatur Sensor-Board, Field 2 = Temperatur Aktor-Board
[daten, zeit] = thingSpeakRead(kanal, 'Fields', [1 2], 'NumPoints', anzahl);

if isempty(daten) || size(daten, 1) < 3
    % Noch zu wenige Daten: Hinweis statt Fehlermeldung
    text(0.5, 0.5, 'Keine Daten im Kanal (Channel ID und Pi pruefen)', ...
        'HorizontalAlignment', 'center');
    axis off;
else
    abweichung = abs(daten(:, 1) - daten(:, 2));            % Differenz beider Sensoren
    glatt      = movmean(abweichung, glaettung, 'omitnan');  % gleitender Mittelwert

    % Trend der geglätteten Abweichung in Grad pro Tag (lineare Regression)
    gueltig = ~isnan(glatt);
    if nnz(gueltig) >= 3
        tage = days(zeit(gueltig) - zeit(find(gueltig, 1)));
        p = polyfit(tage, glatt(gueltig), 1);
        trendText = sprintf('Trend: %+.2f Grad pro Tag', p(1));
    else
        trendText = 'Trend: zu wenige Daten';
    end

    plot(zeit, abweichung, '-', 'Color', [0.80 0.85 0.90]);
    hold on;
    plot(zeit, glatt, '-', 'LineWidth', 2, 'Color', [0.04 0.44 0.64]);
    plot(zeit([1 end]), [schwelle schwelle], '--', 'Color', [0.72 0.36 0.00]);
    hold off;
    grid on;
    ylabel('Abweichung Sensor / Aktor in Grad C');
    title(sprintf('Sensor-Drift (%s)', trendText));
    legend({'Einzelwerte', 'gleitender Mittelwert', 'Warnschwelle'}, 'Location', 'best');
end
