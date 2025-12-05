import request from "supertest";
import app from "../server.js";

describe("API tests", () => {
  it("GET /etudiants should return array", async () => {
    const res = await request(app).get("/etudiants"); // <-- utiliser app directement
    expect(res.statusCode).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
  });
});
