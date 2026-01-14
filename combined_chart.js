  function drawRHRTrend(){
    const canvas = $("rhrTrend");
    if (!canvas) return;
    
    // Combined RHR + HRV chart with dual Y-axes
    requestAnimationFrame(() => {
      const ctx = canvas.getContext("2d");
      const dpr = window.devicePixelRatio || 1;
      
      const rect = canvas.getBoundingClientRect();
      const w = rect.width || 400;
      const h = 160; // Increased height for dual axis
      
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      ctx.scale(dpr, dpr);

      // Collect data from last 12 weeks
      const sorted = [...db.states].sort((a,b) => {
        const aw = (a.weekStart || "").trim();
        const bw = (b.weekStart || "").trim();
        if (aw && bw) return aw.localeCompare(bw);
        return a.updatedAt - b.updatedAt;
      }).slice(-12);

      // Collect RHR data (daily)
      const dailyRHRs = [];
      const dayNames = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
      sorted.forEach(state => {
        const rhrs = state.health?.rhr || [];
        rhrs.forEach((rhr, dayOfWeek) => {
          const val = Number(rhr);
          if (val > 0 && Number.isFinite(val)) {
            dailyRHRs.push({
              value: val,
              week: state.weekStart || new Date(state.updatedAt).toISOString().split('T')[0],
              day: dayNames[dayOfWeek]
            });
          }
        });
      });

      // Collect HRV data and calculate 7-day rolling average
      const dailyHRVs = [];
      sorted.forEach(state => {
        const hrvs = state.health?.hrv || [];
        hrvs.forEach((hrv, dayOfWeek) => {
          const val = Number(hrv);
          if (val > 0 && Number.isFinite(val)) {
            dailyHRVs.push({
              value: val,
              week: state.weekStart || new Date(state.updatedAt).toISOString().split('T')[0],
              day: dayNames[dayOfWeek]
            });
          }
        });
      });

      // Calculate HRV rolling averages
      const hrvRollingAvgs = [];
      for (let i = 0; i < dailyHRVs.length; i++) {
        const start = Math.max(0, i - 6);
        const window = dailyHRVs.slice(start, i + 1);
        const avg = window.reduce((sum, d) => sum + d.value, 0) / window.length;
        hrvRollingAvgs.push({
          value: avg,
          rawValue: dailyHRVs[i].value,
          week: dailyHRVs[i].week,
          day: dailyHRVs[i].day
        });
      }

      // Clear background
      ctx.fillStyle = "rgba(11,13,16,.45)";
      ctx.fillRect(0, 0, w, h);

      // No data check
      if (dailyRHRs.length === 0 && hrvRollingAvgs.length === 0){
        ctx.fillStyle = "rgba(167,179,194,.9)";
        ctx.font = "12px sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText("Start tracking RHR and HRV", w/2, h/2);
        return;
      }

      // Layout
      const leftPad = 45;
      const rightPad = 45; // Room for HRV Y-axis
      const topPad = 15;
      const bottomPad = 12;
      const chartWidth = w - leftPad - rightPad;
      const chartHeight = h - topPad - bottomPad;

      // Determine max data length for x-axis
      const maxLen = Math.max(dailyRHRs.length, hrvRollingAvgs.length);
      const xStep = maxLen > 1 ? chartWidth / (maxLen - 1) : 0;

      // RHR Y-axis scale
      let minRHR = 40, maxRHR = 100, rangeRHR = 60;
      if (dailyRHRs.length > 0) {
        const rhrVals = dailyRHRs.map(d => d.value);
        minRHR = Math.max(40, Math.min(...rhrVals));
        maxRHR = Math.max(...rhrVals);
        minRHR = Math.floor((minRHR - 5) / 5) * 5;
        maxRHR = Math.ceil((maxRHR + 5) / 5) * 5;
        rangeRHR = maxRHR - minRHR;
      }

      const yRHR = (v) => {
        if (rangeRHR === 0) return topPad + chartHeight / 2;
        const t = (v - minRHR) / rangeRHR;
        return topPad + chartHeight - t * chartHeight;
      };

      // HRV Y-axis scale
      let minHRV = 20, maxHRV = 100, rangeHRV = 80;
      if (hrvRollingAvgs.length > 0) {
        const hrvVals = hrvRollingAvgs.map(d => d.value);
        minHRV = Math.max(10, Math.min(...hrvVals));
        maxHRV = Math.max(...hrvVals);
        minHRV = Math.floor((minHRV - 5) / 5) * 5;
        maxHRV = Math.ceil((maxHRV + 5) / 5) * 5;
        rangeHRV = maxHRV - minHRV;
      }

      const yHRV = (v) => {
        if (rangeHRV === 0) return topPad + chartHeight / 2;
        const t = (v - minHRV) / rangeHRV;
        return topPad + chartHeight - t * chartHeight;
      };

      // Draw left Y-axis (RHR)
      ctx.strokeStyle = "rgba(125,211,252,.5)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(leftPad, topPad);
      ctx.lineTo(leftPad, topPad + chartHeight);
      ctx.stroke();

      // RHR Y-axis labels
      ctx.fillStyle = "rgba(125,211,252,.75)";
      ctx.font = "10px monospace";
      ctx.textAlign = "right";
      ctx.textBaseline = "middle";
      const numTicksRHR = 5;
      for (let i = 0; i < numTicksRHR; i++) {
        const val = minRHR + (rangeRHR / (numTicksRHR - 1)) * i;
        const yPos = yRHR(val);
        ctx.fillText(Math.round(val).toString(), leftPad - 6, yPos);
      }

      // Draw right Y-axis (HRV)
      ctx.strokeStyle = "rgba(134,239,172,.5)";
      ctx.beginPath();
      ctx.moveTo(w - rightPad, topPad);
      ctx.lineTo(w - rightPad, topPad + chartHeight);
      ctx.stroke();

      // HRV Y-axis labels
      ctx.fillStyle = "rgba(134,239,172,.75)";
      ctx.textAlign = "left";
      const numTicksHRV = 5;
      for (let i = 0; i < numTicksHRV; i++) {
        const val = minHRV + (rangeHRV / (numTicksHRV - 1)) * i;
        const yPos = yHRV(val);
        ctx.fillText(Math.round(val).toString(), w - rightPad + 6, yPos);
      }

      // Grid lines (subtle)
      ctx.strokeStyle = "rgba(36,48,65,.35)";
      ctx.setLineDash([2, 2]);
      for (let i = 0; i < numTicksRHR; i++) {
        const val = minRHR + (rangeRHR / (numTicksRHR - 1)) * i;
        const yPos = yRHR(val);
        ctx.beginPath();
        ctx.moveTo(leftPad, yPos);
        ctx.lineTo(w - rightPad, yPos);
        ctx.stroke();
      }
      ctx.setLineDash([]);

      // Draw RHR (solid line, blue)
      if (dailyRHRs.length > 0) {
        ctx.strokeStyle = "rgba(125,211,252,.9)";
        ctx.lineWidth = 2;
        ctx.lineJoin = "round";
        ctx.lineCap = "round";
        ctx.beginPath();
        dailyRHRs.forEach((d,i) => {
          const x = leftPad + i*xStep;
          const y = yRHR(d.value);
          if (i===0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        });
        ctx.stroke();

        // Draw RHR points
        dailyRHRs.forEach((d,i) => {
          const x = leftPad + i*xStep;
          const y = yRHR(d.value);
          ctx.fillStyle = "rgba(11,13,16,.9)";
          ctx.beginPath();
          ctx.arc(x, y, 3, 0, Math.PI*2);
          ctx.fill();
          ctx.fillStyle = "rgba(125,211,252,.9)";
          ctx.beginPath();
          ctx.arc(x, y, 2, 0, Math.PI*2);
          ctx.fill();
        });
      }

      // Draw HRV (dotted line, green) - 7-day rolling average
      if (hrvRollingAvgs.length > 0) {
        ctx.strokeStyle = "rgba(134,239,172,.9)";
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 3]);
        ctx.lineJoin = "round";
        ctx.lineCap = "round";
        ctx.beginPath();
        hrvRollingAvgs.forEach((d,i) => {
          const x = leftPad + i*xStep;
          const y = yHRV(d.value);
          if (i===0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        });
        ctx.stroke();
        ctx.setLineDash([]);

        // Draw HRV points
        hrvRollingAvgs.forEach((d,i) => {
          const x = leftPad + i*xStep;
          const y = yHRV(d.value);
          ctx.fillStyle = "rgba(11,13,16,.9)";
          ctx.beginPath();
          ctx.arc(x, y, 3, 0, Math.PI*2);
          ctx.fill();
          ctx.fillStyle = "rgba(134,239,172,.9)";
          ctx.beginPath();
          ctx.arc(x, y, 2, 0, Math.PI*2);
          ctx.fill();
        });
      }

      // Y-axis labels
      ctx.save();
      ctx.fillStyle = "rgba(125,211,252,.7)";
      ctx.font = "10px sans-serif";
      ctx.textAlign = "center";
      ctx.translate(12, topPad + chartHeight / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText("RHR (bpm)", 0, 0);
      ctx.restore();

      ctx.save();
      ctx.fillStyle = "rgba(134,239,172,.7)";
      ctx.translate(w - 12, topPad + chartHeight / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText("HRV 7d (ms)", 0, 0);
      ctx.restore();

      // Legend at bottom
      ctx.fillStyle = "rgba(167,179,194,.5)";
      ctx.font = "10px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(`RHR: ${dailyRHRs.length} days  |  HRV: ${hrvRollingAvgs.length} days (7d avg)`, w/2, h - 3);

      // Hover tooltips - combine both datasets
      const allDataPoints = [];
      dailyRHRs.forEach((d,i) => {
        allDataPoints.push({
          x: leftPad + i*xStep,
          y: yRHR(d.value),
          value: d.value,
          week: d.week,
          day: d.day,
          label: `RHR: ${d.value} bpm`,
          type: 'rhr'
        });
      });
      hrvRollingAvgs.forEach((d,i) => {
        allDataPoints.push({
          x: leftPad + i*xStep,
          y: yHRV(d.value),
          value: Math.round(d.value),
          week: d.week,
          day: d.day,
          label: `HRV: ${Math.round(d.value)} ms (7d) | ${Math.round(d.rawValue)} raw`,
          type: 'hrv'
        });
      });

      setupChartHover(canvas, allDataPoints, w, h, true);
    });
  }

