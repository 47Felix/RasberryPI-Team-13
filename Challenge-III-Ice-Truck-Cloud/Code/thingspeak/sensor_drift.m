% Challenge III: Sensor-Drift (Predictive Maintenance)
% Zweck: Zeigt, ob die beiden Temperatursensoren (Sensor-Board und Aktor-Board) auseinanderlaufen.
%        Eine wachsende Abweichung deutet auf einen defekten Sensor oder einen Wackelkontakt
%        am KY-028 hin. So lässt sich die Wartung planen, bevor der Truck ausfällt.
% Ein Punkt pro Minute (Mittelwert), X-Achse im 1-Minuten-Takt, nur das letzte Zeitfenster.
% Einrichten: ThingSpeak -> Apps -> MATLAB Visualizations -> New -> "Custom (no starting code)",
%             dieses Skript einfügen, "Save and Run".
% Hinweis: Der Kanal ist öffentlich, ein Read Key ist nicht nötig. Bei privatem Kanal bei
%          thingSpeakRead zusätzlich 'ReadKey', '<READ_KEY>' ergänzen (Key nie ins Repository).

kanal      = 3516326;   % Channel ID
anzahl     = 8000;      % letzte Messungen (ThingSpeak liefert höchstens 8000 pro Abruf)
fensterMin = 20;        % angezeigtes Zeitfenster in Minuten
tickMin    = 1;         % Abstand der X-Achsen-Beschriftung in Minuten
glaettung  = 5;         % Minuten pro gleitendem Mittelwert
schwelle   = 3;         % Grad Celsius, entspricht SENSOR_MISMATCH_C in der Bridge

% Field 1 = Temperatur Sensor-Board, Field 2 = Temperatur Aktor-Board
[daten, zeit] = thingSpeakRead(kanal, 'Fields', [1 2], 'NumPoints', anzahl);

% Nur das letzte Zeitfenster anzeigen
if ~isempty(zeit)
    maske = zeit >= zeit(end) - minutes(fensterMin);
    zeit  = zeit(maske);
    daten = daten(maske, :);
end

if isempty(daten) || size(daten, 1) < 3
    % Noch zu wenige Daten: Hinweis statt Fehlermeldung
    text(0.5, 0.5, 'Keine Daten im Kanal (Channel ID und Pi pruefen)', ...
        'HorizontalAlignment', 'center');
    axis off;
else
    % Auf 1-Minuten-Raster mitteln, leere Minuten werden NaN
    tt = timetable(zeit, daten(:, 1), daten(:, 2), 'VariableNames', {'sensor', 'aktor'});
    tt = retime(tt, 'regular', 'mean', 'TimeStep', minutes(1));
    zeitM      = tt.Properties.RowTimes;
    abweichung = abs(tt.sensor - tt.aktor);
    glatt      = movmean(abweichung, glaettung, 'omitnan');
    glatt(isnan(abweichung)) = NaN;   % in Datenluecken keine Linie zeichnen

    % Trend der geglätteten Abweichung in Grad pro Stunde (lineare Regression)
    gueltig = ~isnan(glatt);
    if nnz(gueltig) >= 3
        stunden = hours(zeitM(gueltig) - zeitM(find(gueltig, 1)));
        p = polyfit(stunden, glatt(gueltig), 1);
        trendText = sprintf('Trend: %+.2f Grad pro Stunde', p(1));
    else
        trendText = 'Trend: zu wenige Daten';
    end

    plot(zeitM, abweichung, '-o', 'Color', [0.60 0.70 0.80], 'MarkerSize', 3);
    hold on;
    plot(zeitM, glatt, '-', 'LineWidth', 2, 'Color', [0.04 0.44 0.64]);
    plot(zeitM([1 end]), [schwelle schwelle], '--', 'Color', [0.72 0.36 0.00]);
    hold off;
    grid on;

    % X-Achse im 1-Minuten-Takt
    t0 = dateshift(zeitM(1), 'start', 'minute');
    t1 = dateshift(zeitM(end), 'end', 'minute');
    xlim([t0 t1]);
    xticks(t0:minutes(tickMin):t1);
    xtickformat('HH:mm');
    xtickangle(90);

    xlabel('Uhrzeit (1-Minuten-Takt)');
    ylabel('Abweichung Sensor / Aktor in Grad C');
    title(sprintf('Sensor-Drift, 1-min-Mittel (%s)', trendText));
    legend({'Minutenwerte', sprintf('gleitender Mittelwert (%d min)', glaettung), 'Warnschwelle'}, ...
        'Location', 'best');
end
