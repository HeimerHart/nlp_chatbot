const RefundTimelineCard = ({ data }) => {
  const { stages, current_stage_index: currentIndex, expected_window: window_ } = data;

  return (
    <div className="info-card">
      <div className="info-card-head">
        <span className="eyebrow">Refund timeline</span>
        <span className="demo-tag">Simulated</span>
      </div>
      <div className="refund-track">
        {stages.map((stage, i) => {
          const state = i < currentIndex ? "done" : i === currentIndex ? "active" : "pending";
          return (
            <div className="refund-step" key={stage}>
              <div className={`refund-dot refund-dot-${state}`} />
              <span className={`refund-label refund-label-${state}`}>{stage}</span>
              {i < stages.length - 1 && <div className={`refund-line refund-line-${state}`} />}
            </div>
          );
        })}
      </div>
      <div className="info-card-footer">Expected in {window_}</div>
    </div>
  );
};

export default RefundTimelineCard;
