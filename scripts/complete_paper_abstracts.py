"""Complete paper_abstracts.csv from checked-in PDFs and verified public records."""
import csv
import re
from pathlib import Path

import fitz

LOCAL = {
    "llm_ask": "llm_ask.pdf", "minimum_wage": "minimum_wage.pdf",
    "autopause": "autopause.pdf", "hot_towel": "hot_towel.pdf",
    "uber_price": "uber_price.pdf", "employer_search": "algo_labor_rec.pdf",
    "peer_effects": "peer_effects.pdf", "fruitfly": "dot_guessing_game.pdf",
    "longrun": "longrun.pdf", "olm": "online_labor_markets.pdf",
    "raters": "designing_incentives_for_inexpert_human_raters.pdf",
    "scs": "scs.pdf", "sharing": "sharing.pdf", "spot": "wages_of_paycuts.pdf",
    "standardization": "the_need_for_standardization_in_crowdsourcing.pdf",
    "WageHistory": "WageHistory.pdf",
}

REMOTE = {
    "chaining": ("Production is a sequence of steps that can be executed (1) manually, (2) augmented with AI, or (3) fully automated within contiguous AI-executed steps called “chains.” Firms optimally bundle steps into tasks and then jobs, trading off specialization gains against coordination costs. We characterize the optimal assignment of humans and AI to steps and the firm's resulting job structure, showing that comparative advantage logic can fail with AI chaining. The model implies non-linear productivity gains from AI quality improvements and admits a CES representation at the macro level. Empirical evidence supports the model's key predictions that (1) AI-executed steps co-occur in chains, (2) dispersion of AI-exposed steps lowers AI execution at the job level, and (3) adjacency to AI-executed steps increases the likelihood that a step is AI-executed.", "https://arxiv.org/abs/2606.15960"),
    "spf": ("We develop a framework for simulating professional expectations formation using large language models (LLMs). Combining novel hand-collected data on Survey of Professional Forecasters (SPF) participant characteristics with real-time macroeconomic data and lagged SPF median forecasts, we prompt LLMs to generate quarterly forecasts for 23 variables over 1999–2023. The resulting synthetic panel replicates key properties of the human survey, including forecast accuracy, median forecast levels, revision dynamics, and cross-sectional dispersion. Ablation exercises show that performance is largely driven by information conditioning: removing forecaster characteristics modestly worsens performance, whereas removing real-time data and especially lagged SPF medians leads to substantial error increases. Our framework offers a scalable complement to traditional surveys, enabling counterfactual analysis under alternative information sets, retrospective “as-of” forecasting, and rapid prototyping of survey designs.", "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5066286"),
    "synthetic_labs": ("This paper investigates the behavior of simulated AI agents (large language models, or LLMs) in auctions, introducing a novel synthetic data-generating process to help facilitate the study and design of auctions. We find that LLMs—when endowed with chain-of-thought reasoning capacity—agree with the experimental literature in auctions across a variety of classic auction formats. In particular, LLM bidders produce results consistent with risk-averse human bidders; perform closer to theoretical predictions in obviously strategy-proof auctions; and succumb to the winner's curse in common-value settings. LLMs are not very sensitive to naive prompt changes but can improve dramatically toward theoretical predictions with the right mental model. We run more than 1,000 auctions for less than $400 and develop a flexible framework for further experimental study.", "https://arxiv.org/abs/2507.09083"),
    "ai_bargaining": ("Markets increasingly accommodate large language models (LLMs) as autonomous decision-making agents. We present an empirical study comparing humans, multiple frontier LLMs, and customized Bayesian agents in dynamic multiplayer bargaining games under identical conditions. Bayesian agents extract the highest surplus with aggressive proposals that are frequently rejected. Humans and LLMs achieve comparable aggregate surplus but exhibit different trading strategies: LLMs favor conservative, concessionary proposals, while humans propose trades consistent with fairness norms that are more likely to be rejected. These findings show that performance parity can mask substantive procedural differences in complex multi-agent interactions.", "https://arxiv.org/abs/2509.09071"),
    "jobot": ("Reductions in private search costs due to advances in information technology can theoretically improve market efficiency, but negative externalities can reverse those gains. In a large-scale field experiment on an online labor market, employers randomly offered AI-written first drafts were 19% more likely to post a job and spent 44% less time writing. Despite the increase in postings, matches did not increase. Marginal jobs came from employers with lower hiring intent, and treated posts were more generic and less informative. The resulting dilution of employer-seriousness signals wasted jobseeker time, producing welfare losses per post six times greater than employers' time savings.", "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5187344"),
    "cs": ("AI agents—autonomous systems that perceive, reason, and act on behalf of human principals—are poised to transform digital markets by dramatically reducing transaction costs. This chapter evaluates the economic implications from demand, supply, and market-design perspectives. Users trade off decision quality against effort reduction; firms choose how to design, integrate, and monetize agents; and markets gain from lower search, communication, and contracting costs while facing congestion and price-obfuscation risks. By lowering the costs of preference elicitation, contract enforcement, and identity verification, agents expand the feasible set of market designs but also raise novel regulatory challenges.", "https://www.nber.org/system/files/chapters/c15309/c15309.pdf"),
    "gsa": ("Useful social science theories predict behavior across settings, but applying a theory in new settings often requires ad hoc modifications. We argue that AI agents placed in simulations offer an alternative requiring minimal or no modification. We build “general” agents using theory-grounded natural-language instructions, existing empirical data, and knowledge acquired during model training. To test predictions where no data from the target data-generating process exists, we design a heterogeneous population of 883,320 novel games and construct AI agents using human data from a small set of conceptually related but structurally distinct seed games.", "https://www.nber.org/papers/w34937"),
    "head_in_clouds": ("Crowd computing is the human analogue to cloud computing: where the cloud provides elastic, highly available computation and storage, the crowd provides elastic, highly available human perception and intelligence. This article introduces human computation, surveys the challenges of recruiting and coordinating crowds, and describes opportunities for combining software with human common sense to solve problems that software cannot solve alone.", "papers/head_in_the_clouds.pdf"),
}

def clean(value):
    value = value.translate(str.maketrans({"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"}))
    value = re.sub(r"([A-Za-z])-\s*\n\s*([a-z])", r"\1\2", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value.replace(" - ", "—")

def extract(filename):
    doc = fitz.open(Path("papers") / filename)
    text = "\n".join(page.get_text() for page in doc[:2])
    match = re.search(r"(?ims)^\s*abstract\.?\s*(.*)", text)
    if not match:
        raise ValueError(f"No abstract in {filename}")
    value = match.group(1)
    stops = [r"\n\s*(?:1\s+)?Introduction\b", r"\n\s*Keywords?\b", r"\n\s*Categories and Subject", r"\n\s*ACM Class", r"\n\s*General Terms", r"\n\s*Permission to", r"\n\s*JEL\b", r"\n\s*[∗*†‡§]", r"\n\s*Bios\b"]
    positions = [m.start() for pattern in stops if (m := re.search(pattern, value, re.I))]
    if positions:
        value = value[:min(positions)]
    return clean(value)

path = Path("data/paper_abstracts.csv")
rows = {row["paper_id"]: row for row in csv.DictReader(path.open(newline="", encoding="utf-8"))}
for paper_id, filename in LOCAL.items():
    rows[paper_id] = {"paper_id": paper_id, "abstract": extract(filename), "source_url": f"papers/{filename}"}
for paper_id, (abstract, source_url) in REMOTE.items():
    rows[paper_id] = {"paper_id": paper_id, "abstract": abstract, "source_url": source_url}
with path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["paper_id", "abstract", "source_url"], lineterminator="\n")
    writer.writeheader(); writer.writerows(rows.values())
print(f"Wrote {len(rows)} abstracts")
