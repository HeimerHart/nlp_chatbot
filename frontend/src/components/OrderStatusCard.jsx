const OrderStatusCard = ({ data }) => {
  const { merchant, order_id: orderId, status, eta_minutes: etaMinutes } = data;

  return (
    <div className="info-card">
      <div className="info-card-head">
        <span className="eyebrow">Order status</span>
        <span className="demo-tag">Simulated</span>
      </div>
      <div className="info-card-body">
        <div className="info-row">
          <span className="info-label">Merchant</span>
          <span className="info-value">{merchant}</span>
        </div>
        <div className="info-row">
          <span className="info-label">Order ID</span>
          <span className="info-value info-value-mono">{orderId}</span>
        </div>
        <div className="info-row">
          <span className="info-label">Status</span>
          <span className="info-pill">{status}</span>
        </div>
      </div>
      <div className="info-card-footer">ETA ~{etaMinutes} min</div>
    </div>
  );
};

export default OrderStatusCard;
